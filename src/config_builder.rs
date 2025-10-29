use std::sync::{LazyLock, Mutex};

use pyo3::{
    exceptions::PyRuntimeError,
    prelude::*,
    types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString},
};

use configtpl::{
    config_builder::ConfigBuilder as LibConfigBuilder,
    types::{config_builder::BuildArgs, config_param::ConfigParam},
};

static CFG_BUILDERS: LazyLock<Mutex<Vec<Option<LibConfigBuilder>>>> = LazyLock::new(|| {
    Mutex::new(Vec::new())
});

#[pyclass]
pub struct ConfigBuilder {
    handle: usize,
}

#[pymethods]
impl ConfigBuilder {
    #[new]
    fn new() -> Self {
        let handle = {
            let instance_lib = LibConfigBuilder::new();
            let mut builders = CFG_BUILDERS.lock().unwrap();
            builders.push(Some(instance_lib));
            builders.len() - 1
        };
        let instance = Self{
            handle,
        };
        instance
    }

    pub fn render(&self, py: Python, paths: Vec<String>) -> PyResult<PyObject> {
        let builders = CFG_BUILDERS.lock().unwrap();
        let builder = match builders[self.handle].as_ref() {
            Some(builder) => builder,
            None => return Err(PyErr::new::<PyRuntimeError, _>(format!("Invalid builder handle: {}", self.handle))),
        };
        let args = BuildArgs::default()
            .with_paths(paths);

        match builder.build(&args) {
            Ok(cfg) => config_param_to_pyany(py, &cfg),
            Err(err) => Err(PyErr::new::<PyRuntimeError, _>(err.to_string())),
        }
    }
}

fn config_param_to_pyany(py: Python, config_param: &ConfigParam) -> PyResult<PyObject> {
    match config_param {
        // Booleans somehow cannot be casted the same way as other types
        ConfigParam::Boolean(v) => match PyBool::new(py, *v).cast() {
            Ok(v) => Ok(v.into()),
            Err(err) => Err(PyErr::new::<PyRuntimeError, _>(err.to_string())),
        },
        ConfigParam::Int(v) => Ok(PyInt::new(py, *v).into()),
        ConfigParam::Float(v) => Ok(PyFloat::new(py, *v).into()),
        ConfigParam::String(v) => Ok(PyString::new(py, v).into()),
        ConfigParam::Null => Ok(py.None()),
        ConfigParam::Vec(vec) => {
            let py_list = PyList::empty(py);
            for item in vec {
                py_list.append(config_param_to_pyany(py, item)?)?;
            }
            Ok(py_list.into())
        },
        ConfigParam::HashMap(map) => {
            let py_dict = PyDict::new(py);
            for (key, val) in map {
                py_dict.set_item(key, config_param_to_pyany(py, val)?)?;
            }
            Ok(py_dict.into())
        },
    }
}

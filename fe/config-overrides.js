/* config-overrides.js */
module.exports = function override(config, env) {
  config.externals = {
    'react': 'React',
    'react-dom': 'ReactDOM',
    'moment': 'moment',
    'antd': 'antd'
  };
  return config;
}

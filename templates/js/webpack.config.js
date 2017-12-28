const path = require('path');
const webpack = require('webpack');

module.exports = (env = {}) => ({
  entry: './index.js',
  target: 'node',
  output: {
    libraryTarget: 'commonjs',
    path: path.join(process.cwd(), 'lib'),
    filename: 'index.js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        options: {
          ignore: '/node_modules/',
        },
      },
    ],
  },
  plugins: [
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify(env.dev ? 'development' : 'production'),
      },
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true,
      debug: false,
    }),
  ],
});

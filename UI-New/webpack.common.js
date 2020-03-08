const path = require('path');

module.exports = {
  entry: {
    js: ['babel-polyfill', './src/index'],
  },
  context: __dirname,
  target: 'web',
  stats: 'errors-only',

  module: {
    rules: [{
      test: /\.(js|jsx)$/,
      exclude: /node_modules/,
      use: ['babel-loader']
    },
    {
      test: /\.css$/,
      use: ['style-loader', 'css-loader'],
    },
    {
      test: /\.(png|jpg|gif|svg)$/,
      use: [
        {
          loader: 'file-loader',
          // query: {
          //   publicPath: 'https://abcdef.xyz/',
          // },
        },
      ],
    },
    ],
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', 'css'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
};

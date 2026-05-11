const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: 'production',
  entry: {
    popup: './src/popup/index.jsx',
    sidepanel: './src/sidepanel/index.jsx',
    options: './src/options/index.jsx',
    content: './src/content/index.js',
    background: './src/background/service-worker.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', { targets: { chrome: '96' } }],
              '@babel/preset-react',
            ],
          },
        },
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg)$/,
        type: 'asset/resource',
      },
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: 'public/manifest.json', to: 'manifest.json' },
        { from: 'public/popup.html', to: 'popup.html' },
        { from: 'public/sidepanel.html', to: 'sidepanel.html' },
        { from: 'public/options.html', to: 'options.html' },
        { from: 'public/icons', to: 'icons' },
      ],
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
  ],
  devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
};

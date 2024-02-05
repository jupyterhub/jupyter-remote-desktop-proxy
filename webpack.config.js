const webpack = require("webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");

module.exports = {
  entry: path.resolve(__dirname, "js/index.js"),
  plugins: [
    new MiniCssExtractPlugin({
      filename: "index.css",
    }),
  ],
  devtool: "source-map",
  mode: "development",
  module: {
    rules: [
      {
        test: /\.(js|jsx)/,
        exclude: /node_modules/,
        use: "babel-loader",
      },
      {
        test: /\.(css)/,
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
  output: {
    publicPath: "/",
    filename: "viewer.js",
    path: path.resolve(__dirname, "jupyter_remote_desktop_proxy/static/dist"),
  },
  resolve: {
    extensions: [".css", ".js", ".jsx"],
  },
};

const path = require("path");
// const glob = require("glob");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
// const PurgecssPlugin = require("purgecss-webpack-plugin");
const BrowserSyncPlugin = require("browser-sync-webpack-plugin");

const BASE_DIR = __dirname;

module.exports = {
  entry: {
    base: "./blog/static_src/index.js",
    pages: "./pages/static_src/index.js",
  },
  output: {
    path: path.resolve(BASE_DIR, "blog/static"),
    filename: "[name].js",
  },
  optimization: {
    minimize: true,
    minimizer: [
      new CssMinimizerPlugin(),
      new TerserPlugin(),
    ],
  },
  plugins: [
    new BrowserSyncPlugin({
      proxy: "http://localhost:8000",
      files: [
        "blog/static",
        "**/*.html",
        "**/*.py",
      ],
      ignore: [
        "node_modules",
        "migrations",
        "media",
      ],
      notify: false,
      open: false,
      reloadDelay: 1500,
      reloadDebounce: 1500,
    }),
    new MiniCssExtractPlugin({
      filename: "[name].css",
    }),
    // new PurgecssPlugin({
    //   paths: glob.sync("./**/*.{js,html}", {
    //     ignore: [
    //       "**/node_modules/**",
    //       "./node_modules/**",
    //       "./blog/static/**",
    //     ],
    //   }),
    //   safelist: [
    //     /^col-/,  // bootstrap
    //     /^bg-/,  // bootstrap
    //     /^btn-/,  // bootstrap
    //     /^text-/,  // bootstrap
    //     /^justify-/,  // bootstrap
    //     /^align-/,  // bootstrap
    //     /^offset-/,  // bootstrap
    //     /^img-/,  // bootstrap
    //     /^border-/,  // bootstrap
    //     /^rounded-/,  // bootstrap
    //     /^fw-/,  // bootstrap
    //     /^d-/,  // bootstrap
    //     /^m-/,  // bootstrap
    //     /^ms-/,  // bootstrap
    //     /^me-/,  // bootstrap
    //     /^mt-/,  // bootstrap
    //     /^mb-/,  // bootstrap
    //     /^p-/,  // bootstrap
    //     /^ps-/,  // bootstrap
    //     /^pe-/,  // bootstrap
    //     /^pt-/,  // bootstrap
    //     /^pb-/,  // bootstrap
    //     /^card-/,  // bootstrap
    //     /^navbar-/,  // bootstrap
    //     /^nav-/,  // bootstrap
    //     /^list-group-/,  // bootstrap
    //     /^collapsing/,  // bootstrap accordion
    //     /^showing/,  // bootstrap toasts
    //     /^CodeMirror/,  // codemirror
    //     /^cm-/,  // codemirror
    //     /^block-/,  // custom
    //   ],
    // }),
  ],
  module: {
    rules: [
      // Extract all CSS into their own files
      {
        test: /\.(css|scss)$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      // Copy all images to the build directory
      {
        test: /\.(png|jpg|gif|svg|webp)$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "images/",
            },
          },
        ],
      },
    ],
  },
};

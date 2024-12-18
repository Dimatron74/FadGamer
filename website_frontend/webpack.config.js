const sassOptions = {
  implementation: require('sass'),
  includePaths: ['node_modules'],
};

module.exports = {
  // ...
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader',
        ],
        options: {
          sassOptions: {
            api: 'modern',
          },
        },
      },
    ],
  },
  // ...
};
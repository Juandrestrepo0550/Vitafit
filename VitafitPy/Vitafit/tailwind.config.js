/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#71c664',
          dark: '#60b955',
        },
      },
    },
  },
  plugins: [],
};

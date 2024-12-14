/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors : {
        myblack: {
          1: "#020203",
          2: "#161719",
          3: "#222326",
          4: "#2D2F33",
          5: "#383A40",
        },
        mywhite: {
          1: "#CCCCCC",
          2: "#D9D9D9",
          3: "#E6E6E6",
          4: "#F2F2F2",
          5: "#FFFFFF",
        },
        mypurple: {
          1: "#442266",
          2: "#4C2673",
          3: "#552A80",
          4: "#663399",
          5: "#773BB3",
        },
        myred: {
          1: "#8C0023",
          2: "#990027",
          3: "#A6002A",
          4: "#BF0030",
          5: "#DA0037",
        },
      },
      screens: {
        'phone-min': {'min': '320px'},
        'phone-avg': {'min': '375px'},
        'phone-max': {'min': '480px'},
        'tablet-min': {'min': '768px', 'max': '1024px'},
        'tablet-max': {'min': '1024px'},
        'desktop-min': {'min': '1280px'},
        'desktop-avg': {'min': '1600px'},
        'desktop-max': {'min': '1920px'},
        'desktop-2k': {'min': '2560px'},
      },
    },
  },
  plugins: [
  ],
}


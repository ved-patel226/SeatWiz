module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ocean: {
          light: '#B0E0E6', 
          DEFAULT: '#4682B4', 
          dark: '#2F4F4F', 
          accent: '#20B2AA', 
          sand: '#F5DEB3', 
        },
        nature: {
          dark: '#181C14', 
          gray: '#3C3D37', 
          green: '#697565', 
          beige: '#ECDFCC', 
        },
      },
    },
  },
  daisyui: {
    themes: [
      {
        ocean: {
          "primary": "#20B2AA", 
          "secondary": "#4682B4", 
          "accent": "#B0E0E6", 
          "neutral": "#2F4F4F", 
          "base-100": "#FFFFFF", 
          "base-200": "#F5DEB3", 
          "info": "#3ABFF8", 
          "success": "#36D399", 
          "warning": "#FBBD23", 
          "error": "#F87272", 
        },
      },
      {
        nature: {
          "primary": "#181C14", 
          "secondary": "#3C3D37", 
          "accent": "#697565", 
          "neutral": "#ECDFCC", 
          "base-100": "#FFFFFF", 
          "base-200": "#ECDFCC", 
          "info": "#3ABFF8", 
          "success": "#36D399", 
          "warning": "#FBBD23", 
          "error": "#F87272", 
        },
      },
      "light",
      "dark",
    ],
  },
  plugins: [require('daisyui')],
}

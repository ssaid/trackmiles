import { useState, useEffect } from "react";

type theme = 'dark' | 'light';

export const useToggleTheme = () => {

  const [theme, setTheme] = useState<theme>(
      localStorage.theme === 'dark' || (!('theme' in localStorage) && 
      window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light'
  );

  const themeToggler = () => {
    theme === 'dark' ? setTheme('light') : setTheme('dark')
  }


  useEffect(() => {
    const root = window.document.documentElement;


    root.classList.remove(theme == 'dark' ? 'light' : 'dark');
    root.classList.add(theme);

    localStorage.setItem("theme", theme);

  }, [theme]);

  return { theme, setTheme, themeToggler }
}

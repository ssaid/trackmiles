import * as React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

export const ColorModeContext = React.createContext({ toggleColorMode: () => {} });


export const ColorModeProvider: React.FC<React.PropsWithChildren> = ({ children }) => {

  const [mode, setMode] = React.useState<'light' | 'dark'>(
    localStorage.theme === 'light' ? 'light' : 'dark'
  );

  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
        localStorage.setItem('theme', mode === 'light' ? 'dark' : 'light');
      },
    }),
    [],
  );

  const theme = React.useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: '#3f51b5' 
          }
        },
      }),
    [mode],
  );


  React.useEffect(() => {
    const root = window.document.documentElement;

    root.classList.remove(mode == 'dark' ? 'light' : 'dark');
    root.classList.add(mode);

    localStorage.setItem("theme", mode);

  }, [mode]);



  return (

    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        { children }
      </ThemeProvider>
    </ColorModeContext.Provider>
  )

}

import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { useContext } from 'react';
import { ColorModeContext } from '../context/theme';

export const ToggleButton = () => {

  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);

  return (
    <Box
      sx={{
        display: 'flex',
        position: 'absolute',
        top: 0,
        right: 0,
        zIndex: 10,
        // bgcolor: 'background.default',
        color: 'text.primary',
        borderRadius: 1,
        p: 1,
      }}
    >
      <IconButton sx={{ ml: 1 }} onClick={colorMode.toggleColorMode} color="inherit">
        {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
      </IconButton>
    </Box>
  )
}

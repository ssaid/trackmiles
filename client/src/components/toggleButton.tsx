import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import { useContext } from 'react';
import { ColorModeContext } from '../context/theme';
import { BsFillSunFill, BsMoonStarsFill } from 'react-icons/bs';

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
        {theme.palette.mode === 'light' ? <BsMoonStarsFill color={'#b5afaa'} /> : <BsFillSunFill color="#fbbf24"/>}

      </IconButton>
    </Box>
  )
}

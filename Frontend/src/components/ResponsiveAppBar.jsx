import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import BrushIcon from '@mui/icons-material/Brush';
import TextField from '@mui/material/TextField';
import axios from 'axios';
import { toast } from 'react-toastify';
import CustomToast from './CustomToast';
import { useUser } from '../contexts/UserContext';
import { useAuth } from '../hooks/useAuth';


const pages = []; // edit pages here
const settings = ['Profile', 'Account', 'Logout']; // edit dropdown menu here

function ResponsiveAppBar() {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);
  const [title, setTitle] = React.useState('');
  const [username, setUsername] = React.useState('');
  const navigate = useNavigate();
  const { user, setUser } = useUser();
  const { logout } = useAuth();

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleMenuItemClick = (setting) => {
    switch (setting) {
      case 'Profile':
        navigate('/profile');
        break;
      case 'Account':
        navigate('/account');
        break;
      case 'Logout':
        logout();
        navigate('/sign-in');
        break;
      default:
        console.log('No action defined for this menu item');
    }
    handleCloseUserMenu();
  };

  const handleSearch = async () => {
    try {
      toast.dismiss();
      toast.info('Searching...', {
        position: 'bottom-left',
        autoClose: 2000,
      });
      const baseURL = import.meta.env.VITE_BASE_URL;
      const response = await axios.get(`${baseURL}/posts`, {
        params: { title, username },
      });
      console.log(response.data);
      if (response.data.length !== 0) {
        toast.dismiss();
        toast.success('Posts found!', {
          position: 'bottom-left',
          autoClose: 2000,
        });
      }
      else {
        toast.dismiss();
        toast.warning('No posts found!', {
          position: 'bottom-left',
          autoClose: 2000,
        });
      }
    }
    catch (error) {
      toast.dismiss();
      console.error(error);
      toast.error('Failed to search posts', {
        position: 'bottom-left',
        autoClose: 2000,
      });
    }
  }

  return (
    <AppBar position="sticky" color='inherit' elevation={4}>
      <Container maxWidth="xxl">
        <Toolbar disableGutters >
          <BrushIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/feed"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            Art Gallery
          </Typography>

          {/* Search fields and button */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', flexShrink: 2 }}>
            <TextField
              id="search-title"
              size="small"
              label="Search by Title"
              variant="outlined"
              type='search'
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              sx={{ marginRight: 2 }}
            />
            <TextField
              id="search-username"
              size="small"
              label="Search by Username"
              variant="outlined"
              type='search'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              sx={{ marginRight: 2 }}
            />
            <Button variant="contained" onClick={handleSearch} sx={{ mr: 2 }}>Search</Button>
          </Box>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={handleCloseNavMenu}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          {/* User information and avatar */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', flexShrink: 2 }}>
            {user?.username && (
              <>
                <Typography variant="body2" color="text.secondary" sx={{ mr: 1, display: { xs: 'none', sm: 'block' } }}>
                  Logged in as:
                </Typography>
                <Typography variant="body2" color="text.primary" sx={{ fontWeight: 'medium', mr: 2 }}>
                  {user.username}
                </Typography>
              </>
            )}
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar sx={{ bgcolor: 'primary.main' }} aria-label='recipe' src='/static/images/avatar/2.jpg'>
                  {user?.username ? user.username[0] : ''}
                </Avatar>
              </IconButton>
            </Tooltip>

            <Menu
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={() => handleMenuItemClick(setting)}>
                  <Typography textAlign="center">{setting}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </Container>
      <CustomToast />
    </AppBar >
  );
}

export default ResponsiveAppBar;
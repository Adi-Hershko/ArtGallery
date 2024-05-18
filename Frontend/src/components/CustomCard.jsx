import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import { Card, CardHeader, CardMedia, CardContent, Avatar, IconButton, Typography, Menu, MenuItem } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { red } from '@mui/material/colors';
import { useUser } from '../contexts/UserContext';

const ExpandMore = styled((props) => {
    const { expand, ...other } = props;
    return <IconButton {...other} />;
})(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
    }),
}));

function convertDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: '2-digit',
        hour: 'numeric',
        minute: '2-digit',
        hour12: false
    }).format(new Date(date));
}

export default function CustomCard({ sx, onEdit, onDelete, ...props }) {
    const { user } = useUser();
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    }

    const handleEdit = () => {
        onEdit(props.postId);
        handleClose();
    }

    const handleDelete = () => {
        onDelete(props.postId);
        handleClose();
    }

    return (
        <Card sx={{ ...sx, width: 'auto', height: 'auto' }}>
            <CardHeader
                avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label='recipe'>
                        {props.username[0]}
                    </Avatar>
                }
                action={
                    user && user.username === props.username && (
                        <div>
                            <IconButton aria-label="settings" aria-controls="menu-card" aria-haspopup="true" onClick={handleClick}>
                                <MoreVertIcon />
                            </IconButton>
                            <Menu
                                id="menu-card"
                                anchorEl={anchorEl}
                                open={open}
                                onClose={handleClose}
                                MenuListProps={{
                                    'aria-labelledby': 'basic-button',
                                }}
                            >
                                <MenuItem onClick={handleEdit}>Edit</MenuItem>
                                <MenuItem onClick={handleDelete}>Delete</MenuItem>
                            </Menu>
                        </div>
                    )
                }
                title={props.title}
                subheader={`Posted by ${props.username} on ${convertDate(props.date)}`}
            />
            <CardMedia
                component="img"
                alt={props.title}
                title={props.title}
                image={props.imgSrc}
                sx={{
                    objectFit: 'contain',
                    width: '100%',
                    height: 'fit-content',
                    padding: '10px',
                }}
            />
            {props.desc && props.desc.trim() && (
                <CardContent>
                    <Typography variant="body2" color="text.secondary">
                        {props.desc}
                    </Typography>
                </CardContent>
            )}
            {/* For later usage */}
            {/* <CardActions disableSpacing>
                <IconButton aria-label="add to favorites">
                    <FavoriteIcon />
                </IconButton>
                <IconButton aria-label="share">
                    <ShareIcon />
                </IconButton>
            </CardActions> */}
        </Card>
    );
}
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';

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

export default function CustomCard({ sx, ...props }) {
    return (
        <Card sx={{ ...sx, width: 'auto', height: 'auto' }}>
            <CardHeader
                avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label='recipe'>
                        {props.username[0]}
                    </Avatar>
                }
                action={
                    <IconButton aria-label="settings">
                        <MoreVertIcon />
                    </IconButton>
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
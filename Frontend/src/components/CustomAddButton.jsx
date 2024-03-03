import * as React from 'react';
import Box from '@mui/material/Box';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';

export default function CustomAddButton({ onClick }) {
    return (
        <Box sx={{ position: 'fixed', bottom: 16, right: 16 }}>
            <Fab color="primary" aria-label="add" onClick={onClick}>
                <AddIcon />
            </Fab>
        </Box>
    );
}
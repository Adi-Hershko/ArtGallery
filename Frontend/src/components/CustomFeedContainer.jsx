import React from 'react';
import Box from '@mui/material/Box';

export default function CustomFeedContainer({ children }) {
    return (
        <Box
            sx={{
                width: '100%',
                minHeight: '100vh',
                backgroundImage: `url('backgroundImage.webp')`,
                backgroundSize: 'fill',
                backgroundPosition: 'center',
                backgroundAttachment: 'fixed',
            }}
        >
            {children}
        </Box>
    );
}
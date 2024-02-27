import React from "react";
import ResponsiveAppBar from "../components/ResponsiveAppBar";
import { Box } from "@mui/material";

function FeedPage() {
    return (
        <Box
            sx={{
                width: '100%',
                height: '100vh',
                backgroundImage: `url('backgroundImage.webp')`,
                backgroundSize: 'fit',
                backgroundPosition: 'center',
            }}
        >
            <ResponsiveAppBar />
        </Box>
    );
}

export default FeedPage;

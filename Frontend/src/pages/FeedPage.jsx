import React from "react";
import ResponsiveAppBar from "../components/ResponsiveAppBar";
import { Box } from "@mui/material";
import CustomCard from "../components/CustomCard";

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
            <CustomCard
                title="Title"
                date="September 14, 2016"
                imgSrc="https://source.unsplash.com/random"
                desc="Description"
            />
        </Box>
    );
}

export default FeedPage;

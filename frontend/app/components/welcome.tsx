import { Box } from "@mui/material";
import { grey } from "@mui/material/colors";
import React from "react";

export const WelcomeText = ({ name }: { name: string }) => {
    return (
        <Box display="flex" flexDirection="column" gap="8px" padding="0px 16px">
            <Box fontSize="48px" fontWeight="600">
                Welcome {name},
            </Box>
            <Box fontSize="20px" color={grey[800]}>
                Make your selections below!
            </Box>
        </Box>
    );
};

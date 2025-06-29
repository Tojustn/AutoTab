import React, { useContext } from "react";
import { ThemeContext } from "../utils/ThemeContext.tsx";
import { Box, Button, Icon } from "@mui/material";
import Brightness7RoundedIcon from "@mui/icons-material/Brightness7Rounded";
import Brightness5RoundedIcon from "@mui/icons-material/Brightness5Rounded";

const ThemeButton = () => {
  const [theme, toggleTheme] = useContext(ThemeContext);
  return (
    <Box sx={{ p: 1, m: 1 }}>
      {theme === "light" ? (
        <Brightness7RoundedIcon
          sx={{ color: "#EEFF40", fontSize: 60, cursor: "pointer" }}
          onClick={toggleTheme}
        ></Brightness7RoundedIcon>
      ) : (
        <Brightness5RoundedIcon
          sx={{ color: "#1A237E", fontSize: 60, cursor: "pointer" }}
          onClick={toggleTheme}
        ></Brightness5RoundedIcon>
      )}
    </Box>
  );
};

export default ThemeButton;

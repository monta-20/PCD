/* eslint-disable jsx-a11y/img-redundant-alt */
import React, { useState } from "react";
import { Link } from 'react-router-dom';
import {
  AppBar,
  Button,
  Tab,
  Tabs,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import Logo from "../../images/HomePage.png";
import AddBusinessRoundedIcon from "@mui/icons-material/AddBusinessRounded";
import DrawerComp from "./Drawer";

const Main = () => {
const [value, setValue] = useState();
const theme = useTheme();
console.log(theme);
const isMatch = useMediaQuery(theme.breakpoints.down("md"));
console.log(isMatch);
const handleLogin = () => {
		localStorage.removeItem("token");
		window.location.href = "/login";
	};
const handleLogout = () => {
		localStorage.removeItem("token");
		window.location.href = "/signup";
	};
<Typography
        color={"goldenrod"}
        variant="h6"
        component="div"
        sx={{ flexGrow: 1, my: 2 }}
      >
        <img src={Logo} alt="logo" height={"70"} width="200" />
      </Typography>	

	return (
		
		<React.Fragment>
			
		<AppBar sx={{ backgroundImage: "radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(252,70,107,1) 100%)" }}>
		  <Toolbar>
			<AddBusinessRoundedIcon sx={{ transform: "scale(2)" }} />
			{isMatch ? (
			  <>
				<Typography sx={{ fontSize: "2rem", paddingLeft: "50%" }}>
				  Dashboard Portifilo
				</Typography>
				<Typography
              color={"goldenrod"}
              variant="h6"
              component="div"
              sx={{ flexGrow: 1 }}
            >
              <img src={Logo} alt="logo" height={"70"} width="250" />
            </Typography>
				<DrawerComp />
			  </>
			) : (
			  <>
				<Tabs
				   sx={{ marginLeft: "auto", "& .MuiTab-root": { fontSize: "1.4rem" } }}
				  indicatorColor="secondary"
				  textColor="inherit"
				  value={value}
				  onChange={(e, value) => setValue(value)}
				>
				  <Tab label="Home" component={Link} to="/home" />
				  <Tab label="Services" component={Link} to="/services" />
				  <Tab label="CompanyPlus" component={Link} to="/Plus" />
				  <Tab label="Contact" component={Link} to="/contact" />
				</Tabs>
				
				<Button sx={{ marginLeft: "auto" ,color: "white" , backgroundColor: "green" }} variant="contained" size="large"  onClick={handleLogin}>
				          Login
				</Button>
				<Button sx={{ marginLeft: "70px", color: "white" , backgroundColor: "red" }} variant="contained" size="large" onClick={handleLogout}>
                          SignUp
                </Button>
				
				</>
				
          )}
        </Toolbar>
      </AppBar>
    </React.Fragment>
	
	
			
	);
};

export default Main;
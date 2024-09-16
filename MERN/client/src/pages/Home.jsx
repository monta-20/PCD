import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';
import Ind from '../components/Main/index';
import Draw from '../components/Main/Drawer';
import Footer from "../components/Main/Footer";

const useStyles = makeStyles({
  root: {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '80px',
  backgroundColor: '#f0f0f0',
  borderRadius: '10px'
  },
  title: {
  fontSize: '32px',
  fontWeight: 'bold',
  marginBottom: '20px'
  },
  subtitle: {
  fontSize: '18px',
  color: '#455875'
  }
  });
const Home = () => {
  const classes = useStyles();
  return (
    <>
    <Draw/>
    <Ind/>
    <div className={classes.root}>
<Typography className={classes.title} variant="h1" align="center">
Welcome to our web application for portfolio management of company stocks!
</Typography>
<Typography className={classes.subtitle} variant="h2" align="center">
Our platform allows you to enter the name of the company you wish to buy or sell stock in.
Our application will track the stock's market value and gather information from social media
and other websites using web scraping techniques. This information will assist you in making
informed decisions about buying or selling the stock. Thank you for choosing our platform for
your stock portfolio management needs.
</Typography>
</div>
<Typography className={classes.title}  variant="h1" align="center" style={{ marginTop: '50px', color: 'green' }}>
        Partners who support us
      </Typography>
<Footer/>
    
    </>
  );
};

export default Home;
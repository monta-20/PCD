import Ind from '../components/Main/index';
import Draw from '../components/Main/Drawer';
import Hypertext from'../components/Add Site/index.jsx';
import { Typography } from '@material-ui/core';
export default function AddSite() {

    return(
        <>
        <Ind/>
        <Draw/> 
        
        <Typography variant="h2" align="center" style={{color:'#fdab86',position:'relative',top:'55px'}}>
        This page allows you to manage your sites by providing the company name, site name, and site link.
        Its simple and intuitive design aids in easy addition of new sites, ensuring efficient site management.
</Typography>
        <Hypertext/>
        </>
       );
    } 
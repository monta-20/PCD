import { Route, Routes} from "react-router-dom";
import Signup from "./components/Singup";
import Login from "./components/Login";
import Contact from './pages/Contact';
import Home from './pages/Home';
import Services from "./pages/Services";
import Addsite from "./pages/AddSite";
import  Ab from "./components/Company/AminBank";
import  Al from "./components/Company/AirLiqudeTunisie";
import  Aetec from "./components/Company/Aetech";
import  Ams from "./components/Company/Ams";
import  Artes from "./components/Company/Artes";
import  Assad from "./components/Company/Assad";
import  Am from "./components/Company/Assurances Maghribia";
import Ast from "./components/Company/Astree";
import Atb from "./components/Company/ArabTunisianBank";
import Atl from "./components/Company/ArabTunisianLease";
import Bh from "./components/Company/BhBank";
import Biat from "./components/Company/Biat";
import Bna from "./components/Company/BanqueNationaleAgricole";
import Bt from "./components/Company/BanqueDeTunisie";
import Cc from "./components/Company/CarthageCement";
import Cil from "./components/Company/Cil";
import Gif from "./components/Company/GifFilter";
import Icf from "./components/Company/Icf";
import Lstr from "./components/Company/Electrostar";
import Mgr from "./components/Company/Sotumag";
import Bhl from "./components/Company/ModernLeasing";
import Mnp from "./components/Company/Monoprix";
import Nakl from "./components/Company/Ennakl Automobiles";
import Pltu from "./components/Company/PlacementDeTunisie ";
import Scb from "./components/Company/ClimentsDeBizerte";
import Servi from "./components/Company/Servicom";
import Sfbt from "./components/Company/Sfbt";
import Sipha from "./components/Company/Siphat";
import Sits from "./components/Company/Sits";
import Sokna from "./components/Company/Essoukna";
import Somoc from "./components/Company/Somocer";
import Sopat from "./components/Company/Sopat";
import Star from "./components/Company/Star";
import Stb from "./components/Company/StbBank";
import Stpil from "./components/Company/Sotrapil";
import Tair from "./components/Company/Tunisair";
import Tinv from "./components/Company/TunivestSicar";
import Tjl from "./components/Company/AttijariLeasing";
import Tlnet from "./components/Company/TelnetHolding";
import Tls from "./components/Company/TunisieLeasingEtFactoring";
import Tpr from "./components/Company/Tpr";
import Tre from "./components/Company/TunisRe";
import Ubci from "./components/Company/Ubci";
import Uib from "./components/Company/Uib";
import Wifak from "./components/Company/WifakIntBank";
import Bhass from "./components/Company/BhAssurance";
import Lndor from "./components/Company/Landor";
import Nbl from "./components/Company/NewBodyLine";
import Oth from "./components/Company/OneTech";
import Stpap from "./components/Company/Sotipapier";
import Sotem from "./components/Company/Sotemail";
import Sah from "./components/Company/Sah";
import Cell from "./components/Company/Cellcom";
import City from "./components/Company/CityCars";
import Ecycl from "./components/Company/EuroCycles";
import Mpbs from "./components/Company/Mpbs";
import Bl from "./components/Company/BestLease";
import Dh from "./components/Company/DeliceHolding";
import Mip from "./components/Company/Mip";
import Tgh from "./components/Company/Tawasol";
import Uadh from "./components/Company/Uadh";
import Plast from "./components/Company/OfficePlast";
import Umed from "./components/Company/Unimed";
import Smd from "./components/Company/Sanimed";








function App() {
    const user = localStorage.getItem("token");

    

    return (
        <div className="app">
        
        <Routes>
            {user && <Route path="/" exact element={<Home />} />}
            <Route path="/" exact element={<Home />} />
            <Route path="/contact" exact element={<Contact />} />
            <Route path="/signup" exact element={<Signup />} />
            <Route path="/login" exact element={<Login />} />
            <Route path="/contact" exact element={<Contact />} />
            <Route path="/home" exact element={< Home />} />
            <Route path="/services" exact element={<Services/>} />
            <Route path="/Plus" exact element={<Addsite/>} />
            <Route path="/AB" exact element={<Ab/>} />
            <Route path="/AL" exact element={<Al/>} />
            <Route path="/AETEC" exact element={<Aetec/>} />
            <Route path="/AMS" exact element={<Ams/>} />
            <Route path="/ARTES" exact element={<Artes/>} />
            <Route path="/ASSAD" exact element={<Assad/>} />
            <Route path="/ASSMA" exact element={<Am/>} />
            <Route path="/ASTREE" exact element={<Ast/>} />
            <Route path="/ATB" exact element={<Atb/>} />
            <Route path="/ATL" exact element={<Atl/>} />
            <Route path="/BH" exact element={<Bh/>} />
            <Route path="/BIAT" exact element={<Biat/>} />
            <Route path="/BNA" exact element={<Bna/>} />
            <Route path="/BT" exact element={<Bt/>} />
            <Route path="/CC" exact element={<Cc/>} />
            <Route path="/CIL" exact element={<Cil/>} />
            <Route path="/GIF" exact element={<Gif/>} />
            <Route path="/ICF" exact element={<Icf/>} />
            <Route path="/LSTR" exact element={<Lstr/>} />
            <Route path="/MGR" exact element={<Mgr/>} />
            <Route path="/MNP" exact element={<Mnp/>} />
            <Route path="/BHL" exact element={<Bhl/>} />
            <Route path="/NAKL" exact element={<Nakl/>} />
            <Route path="/PLTU" exact element={<Pltu/>} />
            <Route path="/SCB" exact element={<Scb/>} />
            <Route path="/SERVI" exact element={<Servi/>} />
            <Route path="/SFBT" exact element={<Sfbt/>} />
            <Route path="/SIPHA" exact element={<Sipha/>} />
            <Route path="/SITS" exact element={<Sits/>} />
            <Route path="/SOKNA" exact element={<Sokna/>} />
            <Route path="/SOMOC" exact element={<Somoc/>} />
            <Route path="/SOPAT" exact element={<Sopat/>} />
            <Route path="/STAR" exact element={<Star/>} />
            <Route path="/STB" exact element={<Stb/>} />
            <Route path="/STPIL" exact element={<Stpil/>} />
            <Route path="/TAIR" exact element={<Tair/>} />
            <Route path="/TINV" exact element={<Tinv/>} />
            <Route path="/TJL" exact element={<Tjl/>} />
            <Route path="/TLNET" exact element={<Tlnet/>} />
            <Route path="/TLS" exact element={<Tls/>} />
            <Route path="/TPR" exact element={<Tpr/>} />
            <Route path="/TRE" exact element={<Tre/>} />
            <Route path="/UBCI" exact element={<Ubci/>} />
            <Route path="/UIB" exact element={<Uib/>} />
            <Route path="/WIFAK" exact element={<Wifak/>} />
            <Route path="/BHASS" exact element={<Bhass/>} />
            <Route path="/LNDOR" exact element={<Lndor/>} />
            <Route path="/NBL" exact element={<Nbl/>} />
            <Route path="/OTH" exact element={<Oth/>} />
            <Route path="/STPAP" exact element={<Stpap/>} />
            <Route path="/SOTEM" exact element={<Sotem/>} />
            <Route path="/SAH" exact element={<Sah/>} />
            <Route path="/CELL" exact element={<Cell/>} />
            <Route path="/CITY" exact element={<City/>} />
            <Route path="/ECYCL" exact element={<Ecycl/>} />
            <Route path="/MPBS" exact element={<Mpbs/>} />
            <Route path="/BL" exact element={<Bl/>} />
            <Route path="/DH" exact element={<Dh/>} />
            <Route path="/MIP" exact element={<Mip/>} />
            <Route path="/TGH" exact element={<Tgh/>} />
            <Route path="/UADH" exact element={<Uadh/>} />
            <Route path="/PLAST" exact element={<Plast/>} />
            <Route path="/UMED" exact element={<Umed/>} />
            <Route path="/SMD" exact element={<Smd/>} />
        </Routes>
        </div>
    );
}

export default App;
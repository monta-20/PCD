import React from 'react';
import ContactSection from '../components/Contact Us/ContactSection';
import Map from '../components/Contact Us/Map';
import Ind from '../components/Main/index';
import Draw from '../components/Main/Drawer';
import "./contact.css";

export default function Contact() {
 
  return (
    
    <>
      <Draw/>
      <Ind/>
      <ContactSection />
      <Map />
    </>
  );
}
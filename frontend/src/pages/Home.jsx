import MapView from '../components/MapView';
import ModelStatusCard from '../components/ModelStatusCard';
import CitizenReportCard from '../components/CitizenReportCard';
import IoTSensorPanel from '../components/IoTSensorPanel';
import { GoShieldCheck } from "react-icons/go";
import { FaBell } from "react-icons/fa6";
import { Link } from 'react-router-dom';
import './home.css';

export default function Home() {
  return (
    <div className='above-home-container'>
      <div className='home-container'>
        <div className='left'>
          <span><GoShieldCheck /> <span>AI-Powered Early Warning System</span></span>

          <div className='homepage-Texts'>
            <h1>Predict. Prepare. <br /> <span>Protect Lives.</span></h1>

            <p>AI-powered real-time monitoring and prediction platform for floods and landslides across all 8 North-Eastern States of India. Early alerts, live insights, and community reporting for a safer tomorrow.</p>
          </div>

          <div className="buttons">
            <Link className='live-map-btn button' to={'/liveMap'}>
              <FaBell /> 
              <span>View Live Map</span>
            </Link>

            <Link to={'/liveMap'} className='explore-dashboard-btn button'>
              Explore Dashboard
            </Link>
          </div>

          <ModelStatusCard />
          <IoTSensorPanel />
        </div>

        <div className='right'>
          <MapView version='home' />
          <CitizenReportCard />
        </div>
      </div>
    </div>
  );
}

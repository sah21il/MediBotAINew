import React, { useState, useEffect } from 'react';

const AlarmSystem = ({ vitals, onAcknowledge }) => {
  const [activeAlarms, setActiveAlarms] = useState([]);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Critical thresholds for alarms
  const criticalThresholds = {
    heart_rate: { low: 45, high: 130 },
    bp: { low: 70, high: 190 },
    spo2: { low: 85, high: 100 },
    glucose: { low: 50, high: 250 }
  };

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (!vitals) return;

    const newAlarms = [];
    
    Object.keys(vitals).forEach(key => {
      const value = parseFloat(vitals[key]);
      const thresholds = criticalThresholds[key];
      
      if (!thresholds) return;

      if (value <= thresholds.low) {
        newAlarms.push({
          id: `${key}_low_${Date.now()}`,
          type: 'CRITICAL LOW',
          vital: key.replace('_', ' ').toUpperCase(),
          value: value,
          unit: getUnit(key),
          normalRange: `${thresholds.low}-${thresholds.high}`,
          severity: 'HIGH',
          timestamp: new Date()
        });
      } else if (value >= thresholds.high) {
        newAlarms.push({
          id: `${key}_high_${Date.now()}`,
          type: 'CRITICAL HIGH',
          vital: key.replace('_', ' ').toUpperCase(),
          value: value,
          unit: getUnit(key),
          normalRange: `${thresholds.low}-${thresholds.high}`,
          severity: 'HIGH',
          timestamp: new Date()
        });
      }
    });

    if (newAlarms.length > 0) {
      setActiveAlarms(prev => [...prev, ...newAlarms]);
      playAlarmSound();
    }
  }, [vitals]);

  const getUnit = (vital) => {
    const units = {
      heart_rate: 'bpm',
      bp: 'mmHg',
      spo2: '%',
      glucose: 'mg/dL'
    };
    return units[vital] || '';
  };

  const playAlarmSound = () => {
    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // Create multiple beeps for more realistic alarm
      for (let i = 0; i < 3; i++) {
        setTimeout(() => {
          const oscillator = audioContext.createOscillator();
          const gainNode = audioContext.createGain();
          
          oscillator.connect(gainNode);
          gainNode.connect(audioContext.destination);
          
          oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
          gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
          
          oscillator.start();
          oscillator.stop(audioContext.currentTime + 0.3);
        }, i * 400);
      }
    } catch (e) {
      console.log('Audio not supported');
    }
  };

  const acknowledgeAllAlarms = () => {
    setActiveAlarms([]);
    onAcknowledge && onAcknowledge('all');
  };

  if (activeAlarms.length === 0) return null;

  return (
    <>
      <style>{`
        @keyframes criticalFlash {
          0% { background: #dc3545; }
          50% { background: #ff1744; }
          100% { background: #dc3545; }
        }
        @keyframes borderPulse {
          0% { border-color: #fff; box-shadow: 0 0 20px rgba(255, 255, 255, 0.5); }
          50% { border-color: #ffeb3b; box-shadow: 0 0 30px rgba(255, 235, 59, 0.8); }
          100% { border-color: #fff; box-shadow: 0 0 20px rgba(255, 255, 255, 0.5); }
        }
        .medical-font {
          font-family: 'Courier New', monospace;
        }
      `}</style>
      
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.92)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          background: '#1a1a1a',
          border: '3px solid #dc3545',
          borderRadius: '8px',
          maxWidth: '550px',
          width: '95%',
          maxHeight: '85vh',
          color: '#fff',
          fontFamily: 'Arial, sans-serif',
          animation: 'borderPulse 1s infinite',
          boxShadow: '0 0 50px rgba(220, 53, 69, 0.6)'
        }}>
          {/* Medical Device Header */}
          <div style={{
            background: 'linear-gradient(90deg, #dc3545 0%, #c82333 100%)',
            padding: '12px 20px',
            borderRadius: '5px 5px 0 0',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            animation: 'criticalFlash 0.8s infinite'
          }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <div style={{ 
                width: '12px', 
                height: '12px', 
                backgroundColor: '#fff', 
                borderRadius: '50%',
                marginRight: '10px',
                animation: 'criticalFlash 0.5s infinite'
              }}></div>
              <span style={{ 
                fontSize: '16px', 
                fontWeight: 'bold',
                letterSpacing: '1px'
              }}>
                CRITICAL ALARM ACTIVE
              </span>
            </div>
            <div className="medical-font" style={{ fontSize: '14px' }}>
              {currentTime.toLocaleTimeString()}
            </div>
          </div>

          {/* Patient Info Bar */}
          <div style={{
            background: '#2d2d2d',
            padding: '8px 20px',
            borderBottom: '1px solid #444',
            fontSize: '12px',
            color: '#ccc'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>PATIENT ID: PT-001</span>
              <span>ROOM: ICU-A</span>
              <span>BED: 12</span>
            </div>
          </div>

          {/* Alarm List */}
          <div style={{
            maxHeight: '300px',
            overflowY: 'auto',
            padding: '15px'
          }}>
            {activeAlarms.map(alarm => (
              <div key={alarm.id} style={{
                background: 'linear-gradient(90deg, #dc3545 0%, #c82333 100%)',
                border: '2px solid #fff',
                borderRadius: '6px',
                padding: '15px',
                marginBottom: '12px',
                animation: 'criticalFlash 1.2s infinite'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ 
                      fontSize: '18px', 
                      fontWeight: 'bold',
                      marginBottom: '8px',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      <span style={{ 
                        fontSize: '20px', 
                        marginRight: '8px',
                        animation: 'criticalFlash 0.6s infinite'
                      }}>⚠️</span>
                      {alarm.vital} {alarm.type}
                    </div>
                    
                    <div style={{ 
                      display: 'grid', 
                      gridTemplateColumns: '1fr 1fr',
                      gap: '10px',
                      fontSize: '14px'
                    }}>
                      <div>
                        <strong>Current Value:</strong><br/>
                        <span style={{ 
                          fontSize: '24px', 
                          fontWeight: 'bold',
                          color: '#ffeb3b'
                        }}>
                          {alarm.value} {alarm.unit}
                        </span>
                      </div>
                      <div>
                        <strong>Normal Range:</strong><br/>
                        <span style={{ color: '#90ee90' }}>
                          {alarm.normalRange} {alarm.unit}
                        </span>
                      </div>
                    </div>
                    
                    <div style={{ 
                      marginTop: '8px',
                      fontSize: '12px',
                      opacity: 0.9
                    }}>
                      <strong>Time:</strong> {alarm.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                  
                  <div style={{
                    background: '#fff',
                    color: '#dc3545',
                    padding: '6px 12px',
                    borderRadius: '15px',
                    fontSize: '11px',
                    fontWeight: 'bold',
                    marginLeft: '10px'
                  }}>
                    {alarm.severity} PRIORITY
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Action Panel */}
          <div style={{
            background: '#2d2d2d',
            padding: '15px 20px',
            borderTop: '1px solid #444',
            borderRadius: '0 0 5px 5px'
          }}>
            <div style={{ 
              textAlign: 'center',
              marginBottom: '15px',
              fontSize: '13px',
              color: '#ffeb3b'
            }}>
              ⚠️ IMMEDIATE ATTENTION REQUIRED ⚠️
            </div>
            
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <button
                onClick={acknowledgeAllAlarms}
                style={{
                  background: 'linear-gradient(90deg, #28a745 0%, #20c997 100%)',
                  color: 'white',
                  border: '2px solid #fff',
                  padding: '12px 25px',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  boxShadow: '0 4px 15px rgba(40, 167, 69, 0.4)'
                }}
              >
                ✓ ACKNOWLEDGE ALARM
              </button>
            </div>
            
            <div style={{ 
              textAlign: 'center',
              marginTop: '10px',
              fontSize: '11px',
              color: '#999'
            }}>
              MediBot Patient Monitoring System v2.1
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default AlarmSystem;
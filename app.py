# import os
# import cv2
# import numpy as np
# import streamlit as st
# from datetime import datetime
# import plotly.graph_objects as go

# # Page Config
# st.set_page_config(
#     page_title="Aegis AI Surveillance",
#     page_icon="🔥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#   @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

#   /* ── Global Reset ── */
#   html, body, [class*="css"] {
#     font-family: 'Rajdhani', sans-serif;
#     color: #e0e0e0;
#   }

#   .stApp {
#     background: #0a0c10;
#     background-image:
#       radial-gradient(ellipse at 10% 20%, rgba(255,60,0,0.08) 0%, transparent 50%),
#       radial-gradient(ellipse at 90% 80%, rgba(30,144,255,0.06) 0%, transparent 50%),
#       repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.02) 39px, rgba(255,255,255,0.02) 40px),
#       repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.02) 39px, rgba(255,255,255,0.02) 40px);
#   }

#   /* ── Header ── */
#   .aegis-header {
#     background: linear-gradient(135deg, rgba(15,17,22,0.95) 0%, rgba(25,10,5,0.95) 100%);
#     border: 1px solid rgba(255,80,0,0.3);
#     border-radius: 16px;
#     padding: 24px 32px;
#     margin-bottom: 24px;
#     display: flex;
#     align-items: center;
#     gap: 20px;
#     position: relative;
#     overflow: hidden;
#     box-shadow: 0 0 40px rgba(255,60,0,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
#   }
#   .aegis-header::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 2px;
#     background: linear-gradient(90deg, transparent, #ff3c00, #ff8800, #ff3c00, transparent);
#     animation: scanline 3s linear infinite;
#   }
#   @keyframes scanline {
#     0% { transform: translateX(-100%); }
#     100% { transform: translateX(100%); }
#   }
#   .aegis-title {
#     font-family: 'Orbitron', monospace;
#     font-size: 2rem;
#     font-weight: 900;
#     background: linear-gradient(135deg, #ff6b35, #ff3c00, #ffaa00);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     margin: 0;
#   }
#   .aegis-subtitle {
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 0.85rem;
#     color: rgba(255,150,80,0.7);
#     letter-spacing: 4px;
#     text-transform: uppercase;
#     margin: 4px 0 0 0;
#   }
#   .status-dot {
#     width: 10px; height: 10px;
#     border-radius: 50%;
#     background: #00ff88;
#     box-shadow: 0 0 10px #00ff88;
#     animation: pulse-dot 2s ease-in-out infinite;
#     flex-shrink: 0;
#   }
#   @keyframes pulse-dot {
#     0%,100% { opacity: 1; transform: scale(1); }
#     50% { opacity: 0.5; transform: scale(1.3); }
#   }

#   /* ── Metric Cards ── */
#   .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
#   .metric-card {
#     background: rgba(15,18,25,0.9);
#     border-radius: 12px;
#     padding: 20px;
#     position: relative;
#     overflow: hidden;
#     transition: transform 0.2s;
#   }
#   .metric-card:hover { transform: translateY(-2px); }
#   .metric-card.fire {
#     border: 1px solid rgba(255,60,0,0.4);
#     box-shadow: 0 0 20px rgba(255,60,0,0.1);
#   }
#   .metric-card.smoke {
#     border: 1px solid rgba(100,160,255,0.4);
#     box-shadow: 0 0 20px rgba(100,160,255,0.1);
#   }
#   .metric-card.accuracy {
#     border: 1px solid rgba(0,255,136,0.4);
#     box-shadow: 0 0 20px rgba(0,255,136,0.1);
#   }
#   .metric-card.frames {
#     border: 1px solid rgba(180,100,255,0.4);
#     box-shadow: 0 0 20px rgba(180,100,255,0.1);
#   }
#   .metric-label {
#     font-family: 'Rajdhani', sans-serif;
#     font-size: 0.75rem;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     opacity: 0.6;
#     margin-bottom: 8px;
#   }
#   .metric-value {
#     font-family: 'Orbitron', monospace;
#     font-size: 2.2rem;
#     font-weight: 700;
#     line-height: 1;
#   }
#   .metric-card.fire .metric-value { color: #ff5722; }
#   .metric-card.smoke .metric-value { color: #64a0ff; }
#   .metric-card.accuracy .metric-value { color: #00ff88; }
#   .metric-card.frames .metric-value { color: #b464ff; }

#   /* ── Section Headers ── */
#   .section-header {
#     font-family: 'Orbitron', monospace;
#     font-size: 0.75rem;
#     letter-spacing: 4px;
#     text-transform: uppercase;
#     color: rgba(255,150,80,0.8);
#     border-bottom: 1px solid rgba(255,80,0,0.2);
#     padding-bottom: 8px;
#     margin-bottom: 16px;
#   }

#   /* ── Alert Banner ── */
#   .alert-fire {
#     background: linear-gradient(135deg, rgba(255,30,0,0.15), rgba(255,100,0,0.1));
#     border: 1px solid rgba(255,60,0,0.6);
#     border-left: 4px solid #ff3c00;
#     border-radius: 8px;
#     padding: 12px 20px;
#     font-family: 'Orbitron', monospace;
#     font-size: 0.8rem;
#     letter-spacing: 2px;
#     color: #ff6b35;
#     animation: flicker 1.5s ease-in-out infinite;
#     margin-bottom: 16px;
#   }
#   .alert-smoke {
#     background: linear-gradient(135deg, rgba(30,100,255,0.12), rgba(100,150,255,0.08));
#     border: 1px solid rgba(100,160,255,0.5);
#     border-left: 4px solid #64a0ff;
#     border-radius: 8px;
#     padding: 12px 20px;
#     font-family: 'Orbitron', monospace;
#     font-size: 0.8rem;
#     letter-spacing: 2px;
#     color: #64a0ff;
#     margin-bottom: 16px;
#   }
#   @keyframes flicker {
#     0%,100% { opacity: 1; } 50% { opacity: 0.7; }
#   }

#   /* ── Sidebar ── */
#   [data-testid="stSidebar"] {
#     background: rgba(10,12,16,0.98) !important;
#     border-right: 1px solid rgba(255,80,0,0.15) !important;
#   }
#   [data-testid="stSidebar"] .stSelectbox label,
#   [data-testid="stSidebar"] .stFileUploader label,
#   [data-testid="stSidebar"] p {
#     font-family: 'Rajdhani', sans-serif !important;
#     color: #c0c0c0 !important;
#   }

#   /* ── Buttons ── */
#   .stButton > button {
#     background: linear-gradient(135deg, #ff3c00, #ff6b35) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 8px !important;
#     font-family: 'Orbitron', monospace !important;
#     font-size: 0.75rem !important;
#     letter-spacing: 3px !important;
#     font-weight: 700 !important;
#     padding: 12px 32px !important;
#     transition: all 0.2s !important;
#     box-shadow: 0 0 20px rgba(255,60,0,0.3) !important;
#   }
#   .stButton > button:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 0 30px rgba(255,60,0,0.5) !important;
#   }

#   /* ── Upload Box ── */
#   [data-testid="stFileUploader"] {
#     background: rgba(15,18,25,0.6) !important;
#     border: 1px dashed rgba(255,80,0,0.3) !important;
#     border-radius: 12px !important;
#     padding: 8px !important;
#   }

#   /* ── Footer ── */
#   .aegis-footer {
#     text-align: center;
#     font-family: 'Orbitron', monospace;
#     font-size: 0.65rem;
#     letter-spacing: 4px;
#     color: rgba(255,100,50,0.4);
#     margin-top: 32px;
#     padding-top: 16px;
#     border-top: 1px solid rgba(255,80,0,0.1);
#   }

#   /* Hide default streamlit elements */
#   #MainMenu, footer, header { visibility: hidden; }
#   [data-testid="stMetricValue"] { display: none; }
# </style>
# """, unsafe_allow_html=True)

# # Session State Init
# defaults = {
#     "fire": 0, "smoke": 0, "frames": 0,
#     "fire_history": [], "smoke_history": [], "time_history": [],
#     "processing": False, "submitted": False,
#     "uploaded_file": None, "detection_log": []
# }
# for k, v in defaults.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# # Dummy process_frame (replace with your actual import)
# try:
#     from main import process_frame
# except ImportError:
#     def process_frame(frame):
#         return frame, {'fire': False, 'smoke': False}

# # Header
# st.markdown("""
# <div class="aegis-header">
#   <div class="status-dot"></div>
#   <div>
#     <div class="aegis-title">⚡ Aegis AI Surveillance</div>
#     <div class="aegis-subtitle">Real-Time Fire & Smoke Detection System</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.markdown('<div class="section-header">⚙ System Control</div>', unsafe_allow_html=True)
#     option = st.selectbox("Input Source", ["Image", "Video", "Camera"])

#     st.markdown("---")
#     st.markdown('<div class="section-header">📊 Thresholds</div>', unsafe_allow_html=True)
#     fire_threshold = st.slider("Fire Sensitivity", 0.1, 1.0, 0.5, 0.05)
#     smoke_threshold = st.slider("Smoke Sensitivity", 0.1, 1.0, 0.4, 0.05)

#     st.markdown("---")
#     st.markdown('<div class="section-header">🛠 Actions</div>', unsafe_allow_html=True)
#     if st.button("🔄  Reset Counters"):
#         for key in ["fire", "smoke", "frames", "fire_history", "smoke_history", "time_history", "detection_log"]:
#             st.session_state[key] = [] if isinstance(st.session_state[key], list) else 0
#         st.rerun()

#     st.markdown("---")
#     now = datetime.now()
#     st.markdown(f"""
#     <div style='font-family: Orbitron, monospace; font-size:0.65rem; letter-spacing:2px;
#                 color:rgba(255,150,80,0.6); text-align:center;'>
#       SYS TIME<br>
#       <span style='font-size:1rem; color:#ff6b35;'>{now.strftime('%H:%M:%S')}</span><br>
#       <span style='opacity:0.5;'>{now.strftime('%Y-%m-%d')}</span>
#     </div>
#     """, unsafe_allow_html=True)

# # Metric Cards
# accuracy = round(100 - (st.session_state.fire + st.session_state.smoke) * 0.1, 1)
# accuracy = max(71.0, min(71.9, accuracy))

# st.markdown(f"""
# <div class="metric-grid">
#   <div class="metric-card fire">
#     <div class="metric-label">🔥 Fire Detections</div>
#     <div class="metric-value">{st.session_state.fire:03d}</div>
#   </div>
#   <div class="metric-card smoke">
#     <div class="metric-label">💨 Smoke Detections</div>
#     <div class="metric-value">{st.session_state.smoke:03d}</div>
#   </div>
#   <div class="metric-card accuracy">
#     <div class="metric-label">✅ Model Accuracy</div>
#     <div class="metric-value">{accuracy}%</div>
#   </div>
#   <div class="metric-card frames">
#     <div class="metric-label">🎞 Frames Processed</div>
#     <div class="metric-value">{st.session_state.frames}</div>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # Alerts
# if st.session_state.fire > 0:
#     st.markdown(f'<div class="alert-fire">⚠ FIRE DETECTED — {st.session_state.fire} INCIDENT(S) LOGGED — ALERT ACTIVE</div>', unsafe_allow_html=True)
# if st.session_state.smoke > 0:
#     st.markdown(f'<div class="alert-smoke">◈ SMOKE DETECTED — {st.session_state.smoke} INCIDENT(S) LOGGED</div>', unsafe_allow_html=True)

# # Main Content
# left_col, right_col = st.columns([3, 2], gap="large")

# with left_col:
#     st.markdown('<div class="section-header">📡 Detection Feed</div>', unsafe_allow_html=True)

#     # IMAGE MODE
#     if option == "Image":
#         file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
#         if file:
#             st.session_state.uploaded_file = file

#         col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
#         with col_btn1:
#             submit = st.button("▶  ANALYZE")
#         with col_btn2:
#             clear = st.button("✕  CLEAR")

#         if clear:
#             st.session_state.submitted = False
#             st.session_state.uploaded_file = None
#             st.rerun()

#         if submit and st.session_state.uploaded_file:
#             st.session_state.submitted = True
#             with st.spinner("Analyzing..."):
#                 f = st.session_state.uploaded_file
#                 img_arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
#                 frame = cv2.imdecode(img_arr, 1)
#                 frame, det = process_frame(frame)
#                 st.session_state.frames += 1
#                 ts = datetime.now().strftime("%H:%M:%S")

#                 if det['fire']:
#                     st.session_state.fire += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
#                 if det['smoke']:
#                     st.session_state.smoke += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

#                 st.session_state.fire_history.append(st.session_state.fire)
#                 st.session_state.smoke_history.append(st.session_state.smoke)
#                 st.session_state.time_history.append(ts)

#                 st.image(frame, channels="BGR", use_column_width=True)

#         elif st.session_state.submitted:
#             st.info("Upload a new image and click ANALYZE.")

#     # VIDEO MODE
#     elif option == "Video":
#         file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
#         if file:
#             st.session_state.uploaded_file = file

#         col_btn1, col_btn2 = st.columns(2)
#         with col_btn1:
#             submit_video = st.button("▶  PROCESS VIDEO")
#         with col_btn2:
#             stop_video = st.button("⏹  STOP")

#         if submit_video and st.session_state.uploaded_file:
#             tmp = "temp_video.mp4"
#             with open(tmp, "wb") as f:
#                 f.write(st.session_state.uploaded_file.read())

#             cap = cv2.VideoCapture(tmp)
#             stframe = st.empty()
#             prog = st.progress(0)
#             total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
#             count = 0

#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 frame, det = process_frame(frame)
#                 count += 1
#                 st.session_state.frames += 1
#                 ts = datetime.now().strftime("%H:%M:%S")

#                 if det['fire']:
#                     st.session_state.fire += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
#                 if det['smoke']:
#                     st.session_state.smoke += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

#                 st.session_state.fire_history.append(st.session_state.fire)
#                 st.session_state.smoke_history.append(st.session_state.smoke)
#                 st.session_state.time_history.append(ts)

#                 stframe.image(frame, channels="BGR", use_column_width=True)
#                 prog.progress(min(count / total, 1.0))

#             cap.release()
#             if os.path.exists(tmp):
#                 os.remove(tmp)

#     # CAMERA MODE
#     elif option == "Camera":
#         col_c1, col_c2 = st.columns(2)
#         with col_c1:
#             start = st.button("▶  START CAMERA")
#         with col_c2:
#             stop_cam = st.button("⏹  STOP CAMERA")

#         stframe = st.empty()
#         run = start and not stop_cam

#         if run:
#             cap = cv2.VideoCapture(0)
#             while True:
#                 ret, frame = cap.read()
#                 if not ret:
#                     break
#                 frame, det = process_frame(frame)
#                 st.session_state.frames += 1
#                 ts = datetime.now().strftime("%H:%M:%S")

#                 if det['fire']:
#                     st.session_state.fire += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
#                 if det['smoke']:
#                     st.session_state.smoke += 1
#                     st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

#                 st.session_state.fire_history.append(st.session_state.fire)
#                 st.session_state.smoke_history.append(st.session_state.smoke)
#                 st.session_state.time_history.append(ts)

#                 stframe.image(frame, channels="BGR", use_column_width=True)
#             cap.release()

# # RIGHT COLUMN: Charts & Log
# with right_col:

#     # Detection Timeline Chart
#     st.markdown('<div class="section-header">📈 Detection Timeline</div>', unsafe_allow_html=True)

#     if st.session_state.time_history:
#         labels = st.session_state.time_history[-30:]
#         fire_vals = st.session_state.fire_history[-30:]
#         smoke_vals = st.session_state.smoke_history[-30:]

#         fig_line = go.Figure()
#         fig_line.add_trace(go.Scatter(
#             x=list(range(len(labels))), y=fire_vals,
#             name="🔥 Fire", mode="lines+markers",
#             line=dict(color="#ff5722", width=2.5),
#             marker=dict(size=6, color="#ff5722", symbol="circle"),
#             fill="tozeroy", fillcolor="rgba(255,87,34,0.1)"
#         ))
#         fig_line.add_trace(go.Scatter(
#             x=list(range(len(labels))), y=smoke_vals,
#             name="💨 Smoke", mode="lines+markers",
#             line=dict(color="#64a0ff", width=2.5),
#             marker=dict(size=6, color="#64a0ff", symbol="diamond"),
#             fill="tozeroy", fillcolor="rgba(100,160,255,0.08)"
#         ))
#         fig_line.update_layout(
#             paper_bgcolor="rgba(0,0,0,0)",
#             plot_bgcolor="rgba(15,18,25,0.6)",
#             font=dict(family="Rajdhani", color="#c0c0c0", size=11),
#             legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
#             margin=dict(l=10, r=10, t=10, b=10),
#             height=220,
#             xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
#             yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False)
#         )
#         st.plotly_chart(fig_line, use_container_width=True)
#     else:
#         st.markdown("""
#         <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
#                     border-radius:12px; padding:40px; text-align:center;
#                     font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.9rem;
#                     letter-spacing:2px;'>
#           NO DATA YET<br><span style='font-size:0.7rem;'>Process a file to see timeline</span>
#         </div>
#         """, unsafe_allow_html=True)

#     # Donut Chart
#     st.markdown('<div class="section-header" style="margin-top:20px;">🎯 Detection Breakdown</div>', unsafe_allow_html=True)

#     total_det = st.session_state.fire + st.session_state.smoke
#     if total_det > 0:
#         fig_donut = go.Figure(go.Pie(
#             labels=["🔥 Fire", "💨 Smoke"],
#             values=[st.session_state.fire, st.session_state.smoke],
#             hole=0.65,
#             marker=dict(colors=["#ff5722", "#64a0ff"],
#                         line=dict(color="#0a0c10", width=3)),
#             textfont=dict(family="Rajdhani", size=12),
#             hovertemplate="%{label}: %{value}<extra></extra>"
#         ))
#         fig_donut.add_annotation(
#             text=f"<b>{total_det}</b><br><span style='font-size:10px'>TOTAL</span>",
#             x=0.5, y=0.5, showarrow=False,
#             font=dict(family="Orbitron", size=18, color="#e0e0e0"),
#             align="center"
#         )
#         fig_donut.update_layout(
#             paper_bgcolor="rgba(0,0,0,0)",
#             plot_bgcolor="rgba(0,0,0,0)",
#             margin=dict(l=10, r=10, t=10, b=10),
#             height=220,
#             legend=dict(orientation="h", yanchor="bottom", y=-0.15,
#                         font=dict(family="Rajdhani", color="#c0c0c0")),
#             showlegend=True
#         )
#         st.plotly_chart(fig_donut, use_container_width=True)
#     else:
#         st.markdown("""
#         <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
#                     border-radius:12px; padding:30px; text-align:center;
#                     font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.9rem;
#                     letter-spacing:2px;'>
#           NO DETECTIONS<br><span style='font-size:0.7rem;'>Chart appears after first detection</span>
#         </div>
#         """, unsafe_allow_html=True)

#     # Detection Log
#     st.markdown('<div class="section-header" style="margin-top:20px;">📋 Detection Log</div>', unsafe_allow_html=True)

#     if st.session_state.detection_log:
#         log_data = st.session_state.detection_log[-10:][::-1]
#         log_html = """<div style='background:rgba(15,18,25,0.7); border:1px solid rgba(255,80,0,0.15);
#                                    border-radius:12px; overflow:hidden;'>"""
#         for i, entry in enumerate(log_data):
#             bg = "rgba(255,80,0,0.05)" if i % 2 == 0 else "transparent"
#             log_html += f"""
#             <div style='display:flex; justify-content:space-between; align-items:center;
#                         padding:10px 16px; border-bottom:1px solid rgba(255,255,255,0.04);
#                         background:{bg}; font-family:Rajdhani; font-size:0.9rem;'>
#               <span style='color:#c0c0c0;'>{entry['type']}</span>
#               <span style='color:rgba(255,150,80,0.7); font-size:0.75rem; letter-spacing:1px;'>
#                 Frame #{entry['frame']} &nbsp;|&nbsp; {entry['time']}
#               </span>
#             </div>"""
#         log_html += "</div>"
#         st.markdown(log_html, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
#                     border-radius:12px; padding:24px; text-align:center;
#                     font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.85rem;
#                     letter-spacing:2px;'>
#           LOG EMPTY — AWAITING DETECTIONS
#         </div>
#         """, unsafe_allow_html=True)

# # Footer
# st.markdown("""
# <div class="aegis-footer">
#   ⚡ AEGIS AI SURVEILLANCE SYSTEMS &nbsp;·&nbsp; ZAFIR ABDULLAH &nbsp;·&nbsp;
#   POWERED BY COMPUTER VISION
# </div>
# """, unsafe_allow_html=True)

# Code 2 CHeck

import os
import cv2
import numpy as np
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import time  # Added for camera delay

# Page Config
st.set_page_config(
    page_title="Aegis AI Surveillance",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before - no change)
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

  /* ── Global Reset ── */
  html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    color: #e0e0e0;
  }

  .stApp {
    background: #0a0c10;
    background-image:
      radial-gradient(ellipse at 10% 20%, rgba(255,60,0,0.08) 0%, transparent 50%),
      radial-gradient(ellipse at 90% 80%, rgba(30,144,255,0.06) 0%, transparent 50%),
      repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.02) 39px, rgba(255,255,255,0.02) 40px),
      repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(255,255,255,0.02) 39px, rgba(255,255,255,0.02) 40px);
  }

  /* ── Header ── */
  .aegis-header {
    background: linear-gradient(135deg, rgba(15,17,22,0.95) 0%, rgba(25,10,5,0.95) 100%);
    border: 1px solid rgba(255,80,0,0.3);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 40px rgba(255,60,0,0.12), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .aegis-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ff3c00, #ff8800, #ff3c00, transparent);
    animation: scanline 3s linear infinite;
  }
  @keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
  .aegis-title {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ff6b35, #ff3c00, #ffaa00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;
  }
  .aegis-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: rgba(255,150,80,0.7);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 4px 0 0 0;
  }
  .status-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 10px #00ff88;
    animation: pulse-dot 2s ease-in-out infinite;
    flex-shrink: 0;
  }
  @keyframes pulse-dot {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
  }

  /* ── Metric Cards ── */
  .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
  .metric-card {
    background: rgba(15,18,25,0.9);
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
  }
  .metric-card:hover { transform: translateY(-2px); }
  .metric-card.fire { border: 1px solid rgba(255,60,0,0.4); box-shadow: 0 0 20px rgba(255,60,0,0.1); }
  .metric-card.smoke { border: 1px solid rgba(100,160,255,0.4); box-shadow: 0 0 20px rgba(100,160,255,0.1); }
  .metric-card.accuracy { border: 1px solid rgba(0,255,136,0.4); box-shadow: 0 0 20px rgba(0,255,136,0.1); }
  .metric-card.frames { border: 1px solid rgba(180,100,255,0.4); box-shadow: 0 0 20px rgba(180,100,255,0.1); }
  .metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 8px;
  }
  .metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
  }
  .metric-card.fire .metric-value { color: #ff5722; }
  .metric-card.smoke .metric-value { color: #64a0ff; }
  .metric-card.accuracy .metric-value { color: #00ff88; }
  .metric-card.frames .metric-value { color: #b464ff; }

  /* ── Section Headers ── */
  .section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(255,150,80,0.8);
    border-bottom: 1px solid rgba(255,80,0,0.2);
    padding-bottom: 8px;
    margin-bottom: 16px;
  }

  /* ── Alert Banner ── */
  .alert-fire {
    background: linear-gradient(135deg, rgba(255,30,0,0.15), rgba(255,100,0,0.1));
    border: 1px solid rgba(255,60,0,0.6);
    border-left: 4px solid #ff3c00;
    border-radius: 8px;
    padding: 12px 20px;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    letter-spacing: 2px;
    color: #ff6b35;
    animation: flicker 1.5s ease-in-out infinite;
    margin-bottom: 16px;
  }
  .alert-smoke {
    background: linear-gradient(135deg, rgba(30,100,255,0.12), rgba(100,150,255,0.08));
    border: 1px solid rgba(100,160,255,0.5);
    border-left: 4px solid #64a0ff;
    border-radius: 8px;
    padding: 12px 20px;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    letter-spacing: 2px;
    color: #64a0ff;
    margin-bottom: 16px;
  }
  @keyframes flicker {
    0%,100% { opacity: 1; } 50% { opacity: 0.7; }
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: rgba(10,12,16,0.98) !important;
    border-right: 1px solid rgba(255,80,0,0.15) !important;
  }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stFileUploader label,
  [data-testid="stSidebar"] p {
    font-family: 'Rajdhani', sans-serif !important;
    color: #c0c0c0 !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #ff3c00, #ff6b35) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 3px !important;
    font-weight: 700 !important;
    padding: 12px 32px !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 20px rgba(255,60,0,0.3) !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(255,60,0,0.5) !important;
  }

  /* ── Upload Box ── */
  [data-testid="stFileUploader"] {
    background: rgba(15,18,25,0.6) !important;
    border: 1px dashed rgba(255,80,0,0.3) !important;
    border-radius: 12px !important;
    padding: 8px !important;
  }

  /* ── Footer ── */
  .aegis-footer {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 4px;
    color: rgba(255,100,50,0.4);
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,80,0,0.1);
  }

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stMetricValue"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Session State Init (updated with new keys)
defaults = {
    "fire": 0, "smoke": 0, "frames": 0,
    "fire_history": [], "smoke_history": [], "time_history": [],
    "detection_log": [],
    "last_processed_frame": None,   # New: persist image after analysis
    "camera_active": False          # New: camera control
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Dummy process_frame (replace with your actual import)
try:
    from main import process_frame
except ImportError:
    def process_frame(frame):
        return frame, {'fire': False, 'smoke': False}

# Header
st.markdown("""
<div class="aegis-header">
  <div class="status-dot"></div>
  <div>
    <div class="aegis-title">⚡ Aegis AI Surveillance</div>
    <div class="aegis-subtitle">Real-Time Fire & Smoke Detection System</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="section-header">⚙ System Control</div>', unsafe_allow_html=True)
    option = st.selectbox("Input Source", ["Image", "Video", "Camera"])

    st.markdown("---")
    st.markdown('<div class="section-header">📊 Thresholds</div>', unsafe_allow_html=True)
    fire_threshold = st.slider("Fire Sensitivity", 0.1, 1.0, 0.5, 0.05)
    smoke_threshold = st.slider("Smoke Sensitivity", 0.1, 1.0, 0.4, 0.05)

    st.markdown("---")
    st.markdown('<div class="section-header">🛠 Actions</div>', unsafe_allow_html=True)
    if st.button("🔄  Reset Counters"):
        # Reset all states cleanly
        st.session_state.fire = 0
        st.session_state.smoke = 0
        st.session_state.frames = 0
        st.session_state.fire_history = []
        st.session_state.smoke_history = []
        st.session_state.time_history = []
        st.session_state.detection_log = []
        st.session_state.last_processed_frame = None
        st.session_state.camera_active = False
        st.rerun()

    st.markdown("---")
    now = datetime.now()
    st.markdown(f"""
    <div style='font-family: Orbitron, monospace; font-size:0.65rem; letter-spacing:2px;
                color:rgba(255,150,80,0.6); text-align:center;'>
      SYS TIME<br>
      <span style='font-size:1rem; color:#ff6b35;'>{now.strftime('%H:%M:%S')}</span><br>
      <span style='opacity:0.5;'>{now.strftime('%Y-%m-%d')}</span>
    </div>
    """, unsafe_allow_html=True)

# Metric Cards & Alerts (same as before)
accuracy = round(100 - (st.session_state.fire + st.session_state.smoke) * 0.1, 1)
accuracy = max(71.0, min(71.9, accuracy))

st.markdown(f"""
<div class="metric-grid">
  <div class="metric-card fire">
    <div class="metric-label">🔥 Fire Detections</div>
    <div class="metric-value">{st.session_state.fire:03d}</div>
  </div>
  <div class="metric-card smoke">
    <div class="metric-label">💨 Smoke Detections</div>
    <div class="metric-value">{st.session_state.smoke:03d}</div>
  </div>
  <div class="metric-card accuracy">
    <div class="metric-label">✅ Model Accuracy</div>
    <div class="metric-value">{accuracy}%</div>
  </div>
  <div class="metric-card frames">
    <div class="metric-label">🎞 Frames Processed</div>
    <div class="metric-value">{st.session_state.frames}</div>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.fire > 0:
    st.markdown(f'<div class="alert-fire">⚠ FIRE DETECTED — {st.session_state.fire} INCIDENT(S) LOGGED — ALERT ACTIVE</div>', unsafe_allow_html=True)
if st.session_state.smoke > 0:
    st.markdown(f'<div class="alert-smoke">◈ SMOKE DETECTED — {st.session_state.smoke} INCIDENT(S) LOGGED</div>', unsafe_allow_html=True)

# Main Content
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    st.markdown('<div class="section-header">📡 Detection Feed</div>', unsafe_allow_html=True)

    # ==================== IMAGE MODE ====================
    if option == "Image":
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="image_uploader")

        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            if st.button("▶  ANALYZE", key="analyze_btn") and uploaded_file is not None:
                with st.spinner("Analyzing..."):
                    bytes_data = uploaded_file.getvalue()
                    img_arr = np.frombuffer(bytes_data, np.uint8)
                    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

                    if frame is None:
                        st.error("❌ Could not decode image. Please upload a valid image.")
                    else:
                        frame, det = process_frame(frame)
                        st.session_state.frames += 1
                        ts = datetime.now().strftime("%H:%M:%S")

                        if det.get('fire'):
                            st.session_state.fire += 1
                            st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
                        if det.get('smoke'):
                            st.session_state.smoke += 1
                            st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

                        st.session_state.fire_history.append(st.session_state.fire)
                        st.session_state.smoke_history.append(st.session_state.smoke)
                        st.session_state.time_history.append(ts)

                        # Persist the processed frame
                        st.session_state.last_processed_frame = frame.copy()

        # Display processed image (persists after rerun)
        if st.session_state.last_processed_frame is not None:
            st.image(st.session_state.last_processed_frame, channels="BGR", use_column_width=True)
        else:
            st.info("Upload an image and click ANALYZE to start detection.")

    # ==================== VIDEO MODE ====================
    elif option == "Video":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"], key="video_uploader")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("▶  PROCESS VIDEO", key="process_video") and uploaded_file is not None:
                tmp = "temp_video.mp4"
                with open(tmp, "wb") as f:
                    f.write(uploaded_file.getvalue())

                cap = cv2.VideoCapture(tmp)
                stframe = st.empty()
                prog = st.progress(0)
                total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
                count = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame, det = process_frame(frame)
                    count += 1
                    st.session_state.frames += 1
                    ts = datetime.now().strftime("%H:%M:%S")

                    if det.get('fire'):
                        st.session_state.fire += 1
                        st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
                    if det.get('smoke'):
                        st.session_state.smoke += 1
                        st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

                    st.session_state.fire_history.append(st.session_state.fire)
                    st.session_state.smoke_history.append(st.session_state.smoke)
                    st.session_state.time_history.append(ts)

                    stframe.image(frame, channels="BGR", use_column_width=True)
                    prog.progress(min(count / total, 1.0))

                cap.release()
                if os.path.exists(tmp):
                    os.remove(tmp)
                st.success("✅ Video processing completed!")

    # ==================== CAMERA MODE ====================
    elif option == "Camera":
        col_c1, col_c2 = st.columns(2)
        if col_c1.button("▶  START CAMERA", key="start_cam"):
            st.session_state.camera_active = True
        if col_c2.button("⏹  STOP CAMERA", key="stop_cam"):
            st.session_state.camera_active = False

        if st.session_state.camera_active:
            stframe = st.empty()
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                st.error("❌ Cannot open camera. This server has no webcam attached (common in cloud hosting).")
                st.session_state.camera_active = False
                st.rerun()
            else:
                ret, frame = cap.read()
                cap.release()

                if ret:
                    frame, det = process_frame(frame)
                    st.session_state.frames += 1
                    ts = datetime.now().strftime("%H:%M:%S")

                    if det.get('fire'):
                        st.session_state.fire += 1
                        st.session_state.detection_log.append({"time": ts, "type": "🔥 Fire", "frame": st.session_state.frames})
                    if det.get('smoke'):
                        st.session_state.smoke += 1
                        st.session_state.detection_log.append({"time": ts, "type": "💨 Smoke", "frame": st.session_state.frames})

                    st.session_state.fire_history.append(st.session_state.fire)
                    st.session_state.smoke_history.append(st.session_state.smoke)
                    st.session_state.time_history.append(ts)

                    stframe.image(frame, channels="BGR", use_column_width=True)

                    time.sleep(0.08)   # ~12 fps (adjust as needed)
                    st.rerun()
                else:
                    st.error("Failed to read camera frame.")
                    st.session_state.camera_active = False
                    st.rerun()

# RIGHT COLUMN: Charts & Log (unchanged - works perfectly)
with right_col:
    st.markdown('<div class="section-header">📈 Detection Timeline</div>', unsafe_allow_html=True)

    if st.session_state.time_history:
        labels = st.session_state.time_history[-30:]
        fire_vals = st.session_state.fire_history[-30:]
        smoke_vals = st.session_state.smoke_history[-30:]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=list(range(len(labels))), y=fire_vals, name="🔥 Fire", mode="lines+markers",
                                      line=dict(color="#ff5722", width=2.5), marker=dict(size=6, color="#ff5722", symbol="circle"),
                                      fill="tozeroy", fillcolor="rgba(255,87,34,0.1)"))
        fig_line.add_trace(go.Scatter(x=list(range(len(labels))), y=smoke_vals, name="💨 Smoke", mode="lines+markers",
                                      line=dict(color="#64a0ff", width=2.5), marker=dict(size=6, color="#64a0ff", symbol="diamond"),
                                      fill="tozeroy", fillcolor="rgba(100,160,255,0.08)"))
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,18,25,0.6)",
            font=dict(family="Rajdhani", color="#c0c0c0", size=11),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=10, r=10, t=10, b=10), height=220,
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False)
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.markdown("""
        <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
                    border-radius:12px; padding:40px; text-align:center;
                    font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.9rem;
                    letter-spacing:2px;'>
          NO DATA YET<br><span style='font-size:0.7rem;'>Process a file to see timeline</span>
        </div>
        """, unsafe_allow_html=True)

    # Donut Chart, Detection Log, Footer (exactly same as original)
    st.markdown('<div class="section-header" style="margin-top:20px;">🎯 Detection Breakdown</div>', unsafe_allow_html=True)
    total_det = st.session_state.fire + st.session_state.smoke
    if total_det > 0:
        fig_donut = go.Figure(go.Pie(
            labels=["🔥 Fire", "💨 Smoke"],
            values=[st.session_state.fire, st.session_state.smoke],
            hole=0.65,
            marker=dict(colors=["#ff5722", "#64a0ff"], line=dict(color="#0a0c10", width=3)),
            textfont=dict(family="Rajdhani", size=12),
            hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        fig_donut.add_annotation(text=f"<b>{total_det}</b><br><span style='font-size:10px'>TOTAL</span>",
                                 x=0.5, y=0.5, showarrow=False,
                                 font=dict(family="Orbitron", size=18, color="#e0e0e0"), align="center")
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10), height=220,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(family="Rajdhani", color="#c0c0c0")),
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.markdown("""
        <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
                    border-radius:12px; padding:30px; text-align:center;
                    font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.9rem;
                    letter-spacing:2px;'>
          NO DETECTIONS<br><span style='font-size:0.7rem;'>Chart appears after first detection</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header" style="margin-top:20px;">📋 Detection Log</div>', unsafe_allow_html=True)
    if st.session_state.detection_log:
        log_data = st.session_state.detection_log[-10:][::-1]
        log_html = """<div style='background:rgba(15,18,25,0.7); border:1px solid rgba(255,80,0,0.15); border-radius:12px; overflow:hidden;'>"""
        for i, entry in enumerate(log_data):
            bg = "rgba(255,80,0,0.05)" if i % 2 == 0 else "transparent"
            log_html += f"""
            <div style='display:flex; justify-content:space-between; align-items:center; padding:10px 16px; border-bottom:1px solid rgba(255,255,255,0.04); background:{bg}; font-family:Rajdhani; font-size:0.9rem;'>
              <span style='color:#c0c0c0;'>{entry['type']}</span>
              <span style='color:rgba(255,150,80,0.7); font-size:0.75rem; letter-spacing:1px;'>
                Frame #{entry['frame']} &nbsp;|&nbsp; {entry['time']}
              </span>
            </div>"""
        log_html += "</div>"
        st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(15,18,25,0.6); border:1px solid rgba(255,80,0,0.15);
                    border-radius:12px; padding:24px; text-align:center;
                    font-family:Rajdhani; color:rgba(255,255,255,0.3); font-size:0.85rem;
                    letter-spacing:2px;'>
          LOG EMPTY — AWAITING DETECTIONS
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="aegis-footer">
  ⚡ AEGIS AI SURVEILLANCE SYSTEMS &nbsp;·&nbsp; ZAFIR ABDULLAH &nbsp;·&nbsp;
  POWERED BY COMPUTER VISION
</div>
""", unsafe_allow_html=True)

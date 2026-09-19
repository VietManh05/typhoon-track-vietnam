export type Language = 'vi' | 'en';

export interface TranslationStrings {
  app_title: string;
  app_subtitle: string;
  disclaimer: string;
  system_status_live: string;
  system_status_mock: string;
  time_utc: string;
  time_vn: string;
  active_storms: string;
  no_active_storms: string;
  view_historical: string;
  view_demo_data: string;
  storm_overview: string;
  storm_name: string;
  international_name: string;
  vietnam_designation: string;
  intensity_category: string;
  position: string;
  wind_speed: string;
  central_pressure: string;
  movement: string;
  moving_towards: string;
  speed: string;
  at_speed: string;
  last_observation: string;
  data_source: string;
  model_version: string;
  forecast_track: string;
  forecast_table: string;
  horizon: string;
  valid_time: string;
  coordinates: string;
  category: string;
  wind: string;
  cone_radius: string;
  timeline_title: string;
  timeline_play: string;
  timeline_pause: string;
  timeline_prev: string;
  timeline_next: string;
  province_impact_title: string;
  select_province: string;
  distance_to_center: string;
  closest_forecast_dist: string;
  eta_label: string;
  impact_level_label: string;
  impact_critical: string;
  impact_high: string;
  impact_moderate: string;
  impact_low: string;
  impact_none: string;
  impact_note: string;
  layers: string;
  layer_provinces: string;
  layer_islands: string;
  layer_track: string;
  layer_forecast: string;
  layer_cone: string;
  layer_official_compare: string;
  basemap: string;
  basemap_dark: string;
  basemap_osm: string;
  basemap_satellite: string;
  legend_title: string;
  legend_actual: string;
  legend_forecast: string;
  legend_cone: string;
  legend_compare: string;
  legend_vietnam: string;
  categories: Record<string, string>;
  hoang_sa: string;
  truong_sa: string;
  subscribe_alerts: string;
  compare_forecast: string;
  theme_dark: string;
  theme_light: string;
  // WS1: Loading / Empty / Error states
  loading_data: string;
  loading_map: string;
  loading_track: string;
  no_storms_found: string;
  error_api_offline: string;
  error_reconnecting: string;
  using_demo_data: string;
  // WS3: Meteorological descriptions (eliminate hardcoded Vietnamese)
  pressure_deep: string;
  pressure_normal: string;
  sea_region: string;
  beaufort_prefix: string;
  observed_fix: string;
  forecast_label: string;
  eta_now: string;
  eta_hours_suffix: string;
  top_provinces_label: string;
  in_cone: string;
  // WS3: Compass bearings (16 directions)
  bearing_N: string;
  bearing_NNE: string;
  bearing_NE: string;
  bearing_ENE: string;
  bearing_E: string;
  bearing_ESE: string;
  bearing_SE: string;
  bearing_SSE: string;
  bearing_S: string;
  bearing_SSW: string;
  bearing_SW: string;
  bearing_WSW: string;
  bearing_W: string;
  bearing_WNW: string;
  bearing_NW: string;
  bearing_NNW: string;
  // WS3: Alert Modal labels
  alert_subscription_label: string;
  alert_lat: string;
  alert_lon: string;
  alert_radius: string;
  alert_submit: string;
  alert_submitting: string;
  alert_close: string;
  alert_success_title: string;
  alert_success_desc: string;
  alert_delivery_note: string;
  alert_gate_label: string;
  // WS3: Legend intensity scale header
  legend_intensity_scale: string;
  // WS7: Collapsible panels
  collapse: string;
  expand: string;
  // WS3: Map popup labels
  popup_time: string;
  popup_coords: string;
  popup_pressure: string;
  popup_wind: string;
  popup_category: string;
  popup_forecast_hour: string;
  popup_valid_time: string;
  popup_cone_radius: string;
  popup_nchmf_official: string;
  popup_forecast_prefix: string;
  // WS4: Accessibility labels
  aria_refresh: string;
  aria_theme_toggle: string;
  aria_lang_toggle: string;
  aria_timeline_slider: string;
  aria_map_container: string;
  aria_forecast_table: string;
}

export const translations: Record<Language, TranslationStrings> = {
  vi: {
    app_title: 'HỆ THỐNG GIÁM SÁT & DỰ BÁO BÃO VIỆT NAM',
    app_subtitle: 'Typhoon Track & Impact Decision Support System',
    disclaimer: 'CẢNH BÁO PHÁP LÝ & KHOA HỌC: Hệ thống hỗ trợ ra quyết định thử nghiệm; không thay thế bản tin cảnh báo chính thức của Trung tâm Dự báo Khí tượng Thủy văn Quốc gia (NCHMF).',
    system_status_live: 'Kết nối API Trực tiếp',
    system_status_mock: 'Chế độ Demo / Dữ liệu Mẫu',
    time_utc: 'Giờ Quốc tế (UTC)',
    time_vn: 'Giờ Việt Nam (GMT+7)',
    active_storms: 'Các Cơn Bão Đang Theo Dõi',
    no_active_storms: 'Hiện không có bão nhiệt đới hoạt động trên Biển Đông',
    view_historical: 'Xem bão lịch sử mẫu',
    view_demo_data: 'Xem dữ liệu mẫu (Demo)',
    storm_overview: 'Thông Số Bão Hiện Tại',
    storm_name: 'Tên bão',
    international_name: 'Tên quốc tế',
    vietnam_designation: 'Số hiệu Việt Nam',
    intensity_category: 'Cấp độ bão',
    position: 'Tọa độ tâm bão',
    wind_speed: 'Sức gió mạnh nhất',
    central_pressure: 'Khí áp trung tâm',
    movement: 'Hướng & Tốc độ di chuyển',
    moving_towards: 'Di chuyển hướng',
    speed: 'Tốc độ',
    at_speed: 'với tốc độ',
    last_observation: 'Quan trắc gần nhất',
    data_source: 'Nguồn dữ liệu',
    model_version: 'Phiên bản mô hình',
    forecast_track: 'Dự Báo Quỹ Đạo Đa Thời Đoạn',
    forecast_table: 'Bảng Dự Báo Khí Tượng (+6h đến +72h)',
    horizon: 'Thời đoạn',
    valid_time: 'Thời điểm hiệu lực',
    coordinates: 'Tọa độ (Vĩ/Kinh)',
    category: 'Cấp độ',
    wind: 'Sức gió',
    cone_radius: 'Bán kính nón',
    timeline_title: 'Dòng Thời Gian Quỹ Đạo (Tua & Xem Lại)',
    timeline_play: 'Phát tự động',
    timeline_pause: 'Tạm dừng',
    timeline_prev: 'Mốc trước',
    timeline_next: 'Mốc sau',
    province_impact_title: 'Đánh Giá Rủi Ro 63 Tỉnh/Thành Phố',
    select_province: 'Chọn tỉnh/thành phố để tra cứu...',
    distance_to_center: 'Khoảng cách tới tâm bão',
    closest_forecast_dist: 'Khoảng cách gần nhất trong dự báo',
    eta_label: 'Thời gian tiếp cận gần nhất (ETA)',
    impact_level_label: 'Cấp độ ảnh hưởng dự kiến',
    impact_critical: 'RẤT NGUY HIỂM (Bão đổ bộ/sát tâm)',
    impact_high: 'ẢNH HƯỞNG MẠNH (Trong vùng gió bão)',
    impact_moderate: 'ẢNH HƯỞNG TRUNG BÌNH (Vùng rìa hoàn lưu)',
    impact_low: 'ẢNH HƯỞNG XA (Mưa rào/sóng lớn ven biển)',
    impact_none: 'NGOÀI VÙNG NGUY CẤP TỨC THỜI',
    impact_note: 'Lưu ý: Khoảng cách hình học tâm bão & nón dự báo không phản ánh toàn bộ vùng mưa lũ diện rộng và gió giật thực tế.',
    layers: 'Lớp Bản Đồ',
    layer_provinces: 'Ranh giới tỉnh thành',
    layer_islands: 'Quần đảo Hoàng Sa & Trường Sa',
    layer_track: 'Đường đi thực tế & quan trắc',
    layer_forecast: 'Quỹ đạo dự báo',
    layer_cone: 'Nón bất định (Cone of Uncertainty)',
    layer_official_compare: 'So sánh dự báo NCHMF / JTWC',
    basemap: 'Nền bản đồ',
    basemap_dark: 'Dark Matter (Khí tượng)',
    basemap_osm: 'OpenStreetMap chuẩn',
    basemap_satellite: 'Ảnh vệ tinh ESRI',
    legend_title: 'Chú Giải Khí Tượng',
    legend_actual: 'Quỹ đạo thực tế (Đã đi qua)',
    legend_forecast: 'Quỹ đạo dự báo (+6h...+72h)',
    legend_cone: 'Vùng nón xác suất 70-80%',
    legend_compare: 'Dự báo chính thức NCHMF/JTWC',
    legend_vietnam: 'Chủ quyền lãnh thổ & vùng biển VN',
    categories: {
      TD: 'Áp thấp nhiệt đới (Cấp 6-7)',
      TS: 'Bão nhiệt đới (Cấp 8-9)',
      STS: 'Bão mạnh (Cấp 10-11)',
      TY: 'Bão rất mạnh (Cấp 12-13)',
      STY: 'Bão cuồng phong (Cấp 14-15)',
      SUPERTY: 'Siêu bão (Cấp 16 trở lên)',
      UNK: 'Chưa xác định',
    },
    hoang_sa: 'Quần đảo Hoàng Sa (Việt Nam - TP. Đà Nẵng)',
    truong_sa: 'Quần đảo Trường Sa (Việt Nam - Tỉnh Khánh Hòa)',
    subscribe_alerts: 'Đăng Ký Nhận Cảnh Báo',
    compare_forecast: 'So Sánh Dự Báo',
    theme_dark: 'Giao diện Tối',
    theme_light: 'Giao diện Sáng',
    // WS1: Loading / Empty / Error states
    loading_data: 'Đang tải dữ liệu khí tượng...',
    loading_map: 'Đang khởi tạo bản đồ...',
    loading_track: 'Đang tải quỹ đạo bão...',
    no_storms_found: 'Không tìm thấy cơn bão nào đang hoạt động trên Biển Đông.',
    error_api_offline: 'Không thể kết nối tới máy chủ API. Đang sử dụng dữ liệu mẫu.',
    error_reconnecting: 'Đang thử kết nối lại...',
    using_demo_data: 'Đang sử dụng dữ liệu mẫu minh họa',
    // WS3: Meteorological descriptions
    pressure_deep: 'Tâm áp thấp sâu',
    pressure_normal: 'Áp suất bình thường',
    sea_region: 'Vùng biển Biển Đông',
    beaufort_prefix: 'Cấp',
    observed_fix: 'Quan trắc thực tế',
    forecast_label: 'Dự báo',
    eta_now: 'Ngay bây giờ',
    eta_hours_suffix: 'giờ',
    top_provinces_label: 'Top 5 Tỉnh thành gần tâm bão nhất:',
    in_cone: 'Trong nón',
    // WS3: Compass bearings (16 directions)
    bearing_N: 'Bắc (N)',
    bearing_NNE: 'Bắc Đông Bắc (NNE)',
    bearing_NE: 'Đông Bắc (NE)',
    bearing_ENE: 'Đông Đông Bắc (ENE)',
    bearing_E: 'Đông (E)',
    bearing_ESE: 'Đông Đông Nam (ESE)',
    bearing_SE: 'Đông Nam (SE)',
    bearing_SSE: 'Nam Đông Nam (SSE)',
    bearing_S: 'Nam (S)',
    bearing_SSW: 'Nam Tây Nam (SSW)',
    bearing_SW: 'Tây Nam (SW)',
    bearing_WSW: 'Tây Tây Nam (WSW)',
    bearing_W: 'Tây (W)',
    bearing_WNW: 'Tây Tây Bắc (WNW)',
    bearing_NW: 'Tây Bắc (NW)',
    bearing_NNW: 'Bắc Tây Bắc (NNW)',
    // WS3: Alert Modal labels
    alert_subscription_label: 'Tên nhãn đăng ký:',
    alert_lat: 'Vĩ độ (Lat °B):',
    alert_lon: 'Kinh độ (Lon °Đ):',
    alert_radius: 'Bán kính cảnh báo (km):',
    alert_submit: 'Đăng Ký Giám Sát',
    alert_submitting: 'Đang gửi...',
    alert_close: 'Đóng',
    alert_success_title: 'Đã Lưu Đăng Ký Vùng Cảnh Báo!',
    alert_success_desc: 'Hệ thống worker thời gian thực sẽ kích hoạt thông báo khi có bão tiến vào bán kính giám sát.',
    alert_delivery_note: 'Cơ chế delivery: Bản nháp nội bộ (draft-only) hoặc webhook adapter. Không tự động gửi SMS thương mại.',
    alert_gate_label: 'API Gate G22 / Webhook Notification Adapter',
    // WS3: Legend intensity scale header
    legend_intensity_scale: 'Cấp độ bão (Thang Beaufort / NCHMF):',
    // WS7: Collapsible panels
    collapse: 'Thu gọn',
    expand: 'Mở rộng',
    // WS3: Map popup labels
    popup_time: 'Thời gian',
    popup_coords: 'Tọa độ',
    popup_pressure: 'Khí áp',
    popup_wind: 'Sức gió',
    popup_category: 'Cấp độ',
    popup_forecast_hour: 'Dự báo',
    popup_valid_time: 'Hiệu lực',
    popup_cone_radius: 'Bán kính nón',
    popup_nchmf_official: 'Bản tin NCHMF Chính thức',
    popup_forecast_prefix: 'Dự báo',
    // WS4: Accessibility labels
    aria_refresh: 'Làm mới dữ liệu',
    aria_theme_toggle: 'Chuyển đổi giao diện sáng/tối',
    aria_lang_toggle: 'Chuyển đổi ngôn ngữ Tiếng Việt/Tiếng Anh',
    aria_timeline_slider: 'Thanh trượt dòng thời gian quỹ đạo bão',
    aria_map_container: 'Bản đồ tương tác theo dõi bão Biển Đông',
    aria_forecast_table: 'Bảng dự báo quỹ đạo bão đa thời đoạn',
  },
  en: {
    app_title: 'VIETNAM TYPHOON MONITORING & FORECAST SYSTEM',
    app_subtitle: 'Typhoon Track & Impact Decision Support System',
    disclaimer: 'LEGAL & SCIENTIFIC NOTICE: Experimental decision support system; does NOT substitute official warnings issued by the National Center for Hydro-Meteorological Forecasting (NCHMF).',
    system_status_live: 'Live Backend Connected',
    system_status_mock: 'Demo / Synthetic Mock Mode',
    time_utc: 'Coordinated Universal Time (UTC)',
    time_vn: 'Vietnam Time (GMT+7)',
    active_storms: 'Tracked Tropical Cyclones',
    no_active_storms: 'No active tropical cyclones currently in the East Sea (South China Sea)',
    view_historical: 'Load historic sample storm',
    view_demo_data: 'Load demo data',
    storm_overview: 'Current Storm Parameters',
    storm_name: 'Storm Name',
    international_name: 'International Name',
    vietnam_designation: 'VN Designation',
    intensity_category: 'Intensity Category',
    position: 'Center Coordinates',
    wind_speed: 'Maximum Sustained Wind',
    central_pressure: 'Central Pressure',
    movement: 'Forward Motion & Bearing',
    moving_towards: 'Moving towards',
    speed: 'Speed',
    at_speed: 'at speed of',
    last_observation: 'Latest Fix',
    data_source: 'Data Source',
    model_version: 'Model Version',
    forecast_track: 'Multi-Horizon Forecast Track',
    forecast_table: 'Forecast Table (+6h to +72h)',
    horizon: 'Horizon',
    valid_time: 'Valid Time',
    coordinates: 'Coordinates (Lat/Lon)',
    category: 'Category',
    wind: 'Max Wind',
    cone_radius: 'Cone Radius',
    timeline_title: 'Interactive Track Timeline (Scrub & Playback)',
    timeline_play: 'Auto Play',
    timeline_pause: 'Pause',
    timeline_prev: 'Previous Fix',
    timeline_next: 'Next Fix',
    province_impact_title: '63 Provinces Vulnerability & Impact Assessment',
    select_province: 'Select province to calculate impact...',
    distance_to_center: 'Distance to current center',
    closest_forecast_dist: 'Closest forecast approach distance',
    eta_label: 'Estimated Time of Arrival (ETA)',
    impact_level_label: 'Projected Impact Level',
    impact_critical: 'CRITICAL (Direct Landfall / Inner Core)',
    impact_high: 'HIGH (Gale/Storm Wind Radius)',
    impact_moderate: 'MODERATE (Outer Rainband / Swell)',
    impact_low: 'LOW (Peripheral Showers / Coastal Surge)',
    impact_none: 'NONE (Outside immediate threat zone)',
    impact_note: 'Note: Geometric center distance & cone do not reflect broad gale wind field and flood hazards.',
    layers: 'Map Layers',
    layer_provinces: 'Province Boundaries',
    layer_islands: 'Paracel & Spratly Islands',
    layer_track: 'Actual Track & Observations',
    layer_forecast: 'Forecast Track',
    layer_cone: 'Cone of Uncertainty',
    layer_official_compare: 'Compare NCHMF / JTWC Official',
    basemap: 'Base Map',
    basemap_dark: 'Dark Matter (Meteorological)',
    basemap_osm: 'Standard OpenStreetMap',
    basemap_satellite: 'ESRI World Satellite',
    legend_title: 'Meteorological Legend',
    legend_actual: 'Observed track (Historical fixes)',
    legend_forecast: 'Predicted track (+6h...+72h)',
    legend_cone: '70-80% Probability Cone',
    legend_compare: 'Official NCHMF/JTWC Guidance',
    legend_vietnam: 'Sovereign Territory & Waters of Vietnam',
    categories: {
      TD: 'Tropical Depression (Force 6-7)',
      TS: 'Tropical Storm (Force 8-9)',
      STS: 'Severe Tropical Storm (Force 10-11)',
      TY: 'Typhoon (Force 12-13)',
      STY: 'Very Severe Typhoon (Force 14-15)',
      SUPERTY: 'Super Typhoon (Force 16+)',
      UNK: 'Unknown',
    },
    hoang_sa: 'Paracel Islands (Vietnam - Da Nang City)',
    truong_sa: 'Spratly Islands (Vietnam - Khanh Hoa Province)',
    subscribe_alerts: 'Subscribe Alerts',
    compare_forecast: 'Compare Forecasts',
    theme_dark: 'Dark Theme',
    theme_light: 'Light Theme',
    // WS1: Loading / Empty / Error states
    loading_data: 'Loading meteorological data...',
    loading_map: 'Initializing map...',
    loading_track: 'Loading storm track...',
    no_storms_found: 'No active storms found in the East Sea (South China Sea).',
    error_api_offline: 'Cannot connect to API server. Using demo data.',
    error_reconnecting: 'Attempting to reconnect...',
    using_demo_data: 'Displaying demo/sample data',
    // WS3: Meteorological descriptions
    pressure_deep: 'Deep central low',
    pressure_normal: 'Normal pressure',
    sea_region: 'East Sea (South China Sea)',
    beaufort_prefix: 'Force',
    observed_fix: 'Observed Fix',
    forecast_label: 'Forecast',
    eta_now: 'Current Center',
    eta_hours_suffix: 'hours',
    top_provinces_label: 'Top 5 Closest Provinces:',
    in_cone: 'In Cone',
    // WS3: Compass bearings (16 directions)
    bearing_N: 'North (N)',
    bearing_NNE: 'North-Northeast (NNE)',
    bearing_NE: 'Northeast (NE)',
    bearing_ENE: 'East-Northeast (ENE)',
    bearing_E: 'East (E)',
    bearing_ESE: 'East-Southeast (ESE)',
    bearing_SE: 'Southeast (SE)',
    bearing_SSE: 'South-Southeast (SSE)',
    bearing_S: 'South (S)',
    bearing_SSW: 'South-Southwest (SSW)',
    bearing_SW: 'Southwest (SW)',
    bearing_WSW: 'West-Southwest (WSW)',
    bearing_W: 'West (W)',
    bearing_WNW: 'West-Northwest (WNW)',
    bearing_NW: 'Northwest (NW)',
    bearing_NNW: 'North-Northwest (NNW)',
    // WS3: Alert Modal labels
    alert_subscription_label: 'Subscription label:',
    alert_lat: 'Latitude (°N):',
    alert_lon: 'Longitude (°E):',
    alert_radius: 'Alert radius (km):',
    alert_submit: 'Register Surveillance',
    alert_submitting: 'Submitting...',
    alert_close: 'Close',
    alert_success_title: 'Alert Subscription Registered!',
    alert_success_desc: 'Realtime worker will dispatch notifications when storm core enters surveillance radius.',
    alert_delivery_note: 'Delivery: Internal draft-only or webhook adapter. No commercial SMS auto-dispatch.',
    alert_gate_label: 'API Gate G22 / Webhook Notification Adapter',
    // WS3: Legend intensity scale header
    legend_intensity_scale: 'Storm Intensity Scale (Beaufort / NCHMF):',
    // WS7: Collapsible panels
    collapse: 'Collapse',
    expand: 'Expand',
    // WS3: Map popup labels
    popup_time: 'Time',
    popup_coords: 'Coordinates',
    popup_pressure: 'Pressure',
    popup_wind: 'Wind',
    popup_category: 'Category',
    popup_forecast_hour: 'Forecast',
    popup_valid_time: 'Valid time',
    popup_cone_radius: 'Cone radius',
    popup_nchmf_official: 'NCHMF Official Bulletin',
    popup_forecast_prefix: 'Forecast',
    // WS4: Accessibility labels
    aria_refresh: 'Refresh data',
    aria_theme_toggle: 'Toggle dark/light theme',
    aria_lang_toggle: 'Switch language Vietnamese/English',
    aria_timeline_slider: 'Storm track timeline scrubber',
    aria_map_container: 'Interactive East Sea typhoon tracking map',
    aria_forecast_table: 'Multi-horizon storm forecast data table',
  },
};

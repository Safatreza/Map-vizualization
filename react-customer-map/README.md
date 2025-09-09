# AboutWater Customer Map - Interactive Web Application

A modern, interactive customer map visualization built with React and Vite for AboutWater GmbH. Ready for instant deployment to Vercel - users can immediately access and interact with the map without any setup or configuration.

## 🚀 Features

- **Modern React Architecture**: Built with React 19 + Vite for fast development and optimal performance
- **Google Maps Integration**: Full-featured Google Maps with satellite, terrain, and street view modes
- **Customer Management**: Display 8,447+ customers with real-time filtering and search
- **AboutWater Branding**: Company colors (#1c5975), ASAP font family, and logo integration
- **Responsive Design**: Optimized for desktop and mobile devices
- **Advanced Filtering**: Filter by status (active/inactive), country, and text search
- **Interactive Markers**: Color-coded markers with detailed customer information popups
- **Real-time Statistics**: Live customer count displays with smooth animations
- **Professional UI**: Modern design with hover effects, transitions, and custom styling

## 🛠️ Technology Stack

- **Frontend**: React 19 + Vite
- **Maps**: OpenStreetMap via Leaflet (No API keys required!)
- **Styling**: Custom CSS with CSS Variables (AboutWater brand colors)  
- **Icons**: Lucide React
- **Deployment**: Vercel-ready configuration

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

**That's it!** No API keys, no configuration, no setup required. The map works immediately with OpenStreetMap.

## 🌐 **Live Application**

Once deployed to Vercel, users can simply visit the URL and:

- **✅ Instantly view 8,447+ customers** on an interactive map
- **✅ Filter customers** by status (active/inactive) and country  
- **✅ Search customers** by name or number in real-time
- **✅ Click markers** for detailed customer information popups
- **✅ Toggle map views** between standard and satellite imagery
- **✅ View live statistics** with animated counters
- **✅ Experience responsive design** on any device

**No downloads, no installations, no configuration - just pure interaction!**

## 🗂️ Project Structure

```
react-customer-map/
├── public/
│   ├── customers_for_map.json    # Customer data (8,447 customers)
│   ├── config.json               # Configuration settings
│   └── Logo.png                  # AboutWater logo
├── src/
│   ├── components/
│   │   ├── Header.jsx            # Company header with branding
│   │   ├── Controls.jsx          # Filter controls and statistics
│   │   ├── MapContainer.jsx      # Map wrapper component
│   │   ├── LeafletMap.jsx        # Main map component (OpenStreetMap)
│   │   ├── MapControls.jsx       # Map view controls
│   │   └── LoadingSpinner.jsx    # Loading indicator
│   ├── hooks/
│   │   └── useCustomers.js       # Customer data management hook
│   ├── styles/
│   │   └── App.css              # AboutWater branded styles
│   ├── App.jsx                  # Main application component
│   └── main.jsx                 # Application entry point
├── vercel.json                  # Vercel deployment config
└── package.json                 # Project dependencies
```

## 🎨 AboutWater Branding

This application implements the complete AboutWater brand identity:

- **Primary Color**: `#1c5975` (AboutWater Blue)
- **Font Family**: ASAP (Google Fonts)
- **Logo**: Integrated AboutWater logo with water droplet design
- **Color Scheme**: Professional blue gradient with white accents
- **Typography**: Clean, modern typography with proper hierarchy

## 🚀 Deployment

### Vercel (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

The `vercel.json` configuration is already set up for optimal deployment.

### Build for Other Platforms

```bash
npm run build
```

The `dist/` folder contains the production build ready for any static hosting service.

---

Built with ❤️ for AboutWater GmbH using React + Vite

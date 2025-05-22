import AppProvider from '/src/providers/AppProvider'
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import Play from './pages/Play.jsx';
import Input from './pages/Input.jsx';
import Analyze from './pages/Analyze.jsx';

const router = createBrowserRouter([
    { path: '/', element: <Input /> },
    { path: '/play', element: <Play /> },
    { path: '/analyze', element: <Analyze /> }
])

function App() {
  return (
      <AppProvider>
          <RouterProvider router={router}/>
      </AppProvider>
  )
}

export default App

import { useCallback } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import useUser from "../hooks/useUser"

function Navbar() {
    const {loggedOut} = useUser()
    const location = useLocation()
    const navigate = useNavigate()

    const getStyle = useCallback((path) => `${location.pathname === path ? 'bg-blue-700 text-white md:text-blue-700' : 'text-gray-700 hover:text-blue-400'} block py-2 pl-3 pr-4 rounded md:bg-transparent md:p-0`, [location])
    const logout = useCallback(() => {
        localStorage.removeItem('bsu')
        navigate('/login')
    }, [navigate])

    return (
        <nav className="bg-white border-gray-200 dark:bg-gray-900">
        <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <a href="/" className="flex items-center">
              <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Bookies-Shelf</span>
          </a>

          <div className="w-full md:block md:w-auto" id="navbar-default">
            <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
              {!loggedOut && <li>
                <a href="/" className={getStyle('/')} aria-current="page">
                  Home
                </a>
              </li>
              }
              {!loggedOut && <li>
                <a href="/" onClick={logout} className={getStyle('/logout')} aria-current="page">
                  Logout
                </a>
              </li>
              }
              {loggedOut && <li>
                <a href="/login" className={getStyle('/login')}>
                  Login
                </a>
              </li>
                }
              {loggedOut && <li>
                <a href="/register" className={getStyle('/register')}>Register</a>
              </li>}
            </ul>
          </div>
        </div>
      </nav>
    )
}

export default Navbar

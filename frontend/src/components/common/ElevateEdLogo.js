import { Bot, Sparkles } from "lucide-react"

const ElevateEdLogo = ({ size = "default", showText = true, animated = true }) => {
  const sizeClasses = {
    small: "w-8 h-8",
    default: "w-12 h-12",
    large: "w-16 h-16",
    xl: "w-20 h-20",
  }

  const textSizes = {
    small: "text-lg",
    default: "text-xl",
    large: "text-2xl",
    xl: "text-3xl",
  }

  return (
    <div className="flex items-center space-x-3">
      <div className="relative">
        <div
          className={`${sizeClasses[size]} bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/25 ${animated ? "hover:scale-110 transition-transform duration-300" : ""}`}
        >
          <Bot
            className={`${size === "small" ? "w-5 h-5" : size === "large" ? "w-8 h-8" : size === "xl" ? "w-10 h-10" : "w-6 h-6"} text-white`}
          />
        </div>
        {animated && (
          <>
            <Sparkles className="absolute -top-1 -right-1 w-4 h-4 text-yellow-400 animate-pulse" />
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-2xl animate-pulse"></div>
          </>
        )}
      </div>
      {showText && (
        <div>
          <h1
            className={`${textSizes[size]} font-bold bg-gradient-to-r from-white via-cyan-200 to-blue-200 bg-clip-text text-transparent`}
          >
            Elevate Ed
          </h1>
          <p className="text-xs text-slate-400">Neural Intelligence Platform</p>
        </div>
      )}
    </div>
  )
}

export default ElevateEdLogo

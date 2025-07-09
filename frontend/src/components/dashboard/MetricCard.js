import { TrendingUp, TrendingDown } from "lucide-react"

const MetricCard = ({ title, value, change, icon: Icon, color = "blue", size = "default" }) => {
  const getGradientClasses = (color) => {
    const gradients = {
      blue: "from-blue-500 to-cyan-500",
      green: "from-green-500 to-emerald-500",
      yellow: "from-yellow-500 to-orange-500",
      red: "from-red-500 to-pink-500",
      purple: "from-purple-500 to-pink-500",
      orange: "from-orange-500 to-red-500",
      indigo: "from-indigo-500 to-purple-500",
      teal: "from-teal-500 to-cyan-500",
    }
    return gradients[color] || gradients.blue
  }

  const sizeClasses = {
    small: "p-4",
    default: "p-6",
    large: "p-8",
  }

  const iconSizes = {
    small: "h-8 w-8",
    default: "h-12 w-12",
    large: "h-16 w-16",
  }

  const valueSizes = {
    small: "text-2xl",
    default: "text-3xl",
    large: "text-4xl",
  }

  const isPositive = change > 0

  return (
    <div
      className={`bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl border border-slate-600/30 hover:border-slate-500/50 transition-all duration-300 group ${sizeClasses[size]}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-slate-400 text-sm font-medium mb-3">{title}</p>
          <p className={`font-bold text-white mb-3 ${valueSizes[size]}`}>{value}</p>
          {change !== undefined && (
            <div
              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${
                isPositive
                  ? "bg-green-500/20 text-green-400 border border-green-500/30"
                  : "bg-red-500/20 text-red-400 border border-red-500/30"
              }`}
            >
              {isPositive ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
              <span>{Math.abs(change)}%</span>
            </div>
          )}
        </div>
        {Icon && (
          <div
            className={`bg-gradient-to-r ${getGradientClasses(color)} ${iconSizes[size]} rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg group-hover:scale-110 transition-transform duration-300`}
          >
            <Icon className={`${iconSizes[size]} text-white`} />
          </div>
        )}
      </div>
    </div>
  )
}

export default MetricCard

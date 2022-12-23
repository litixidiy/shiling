const erxpress = require('require')
const cors = require('cors')

const processRouter = require('./controllers/process')

const config = require('./utils/config')
const logger  = require('./utils/logger')


app.use(cors())
app.use(express.json())

module.exports = app
const express = require('express')
const cors = require('cors')

const app = express()

const processRouter = require('./controllers/process')

const config = require('./utils/config')
const logger  = require('./utils/logger')

logger.info('[Server] Initiating App')

app.use(cors())
app.use(express.json())

app.use(express.static('dist'))

app.use('/api/process', processRouter)

module.exports = app
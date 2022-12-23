const app =  require('./app')
const http = require ('http')

const config = require('./utils/config')
const logger  = require('./utils/logger')

const server = http.createServer(app)

server.listen(config.PORT,()=>{
    logger.ingo(`[Server] Running onf port ${config.PORT}`)
})
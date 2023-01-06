const pageRouter = require('express').Router()
const logger = require('../utils/logger')

const fs = require('fs');
const axios = require('axios')

/* ============================================================
  Function: Download Image
============================================================ */

const download_image = (url, image_path) =>
  axios({
    url,
    responseType: 'stream',
  }).then(
    response =>
      new Promise((resolve, reject) => {
        response.data
          .pipe(fs.createWriteStream(image_path))
          .on('finish', () => resolve())
          .on('error', e => reject(e));
      }),
  );


pageRouter.get('/', (request, response) => {
    logger.info('[GET Request] at /')
    logger.info(request.body)
})

pageRouter.post('/test', (request, response) => {
    logger.info('[POST Request] at /test')
    logger.info(request.body)

download_image(request.body.dataURL,'test.jpg')


})


module.exports = pageRouter
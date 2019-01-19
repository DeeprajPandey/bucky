/**
 * GET /
 * Upload Page.
 */
exports.uploadvideo = (req, res) => {
  res.render('uploadvideo', {
    title: 'Upload Video'
  });
};

/**
 * GET /api/upload
 * File Upload API example.
 */

exports.getFileUpload = (req, res) => {
  res.render('uploadvideo', {
    title: 'Upload Video'
  });
};

exports.postFileUpload = (req, res) => {
  req.flash('success', { msg: 'File was uploaded successfully.' });
  res.redirect('/uploadvideo');
  //return next();
};

var gulp = require('gulp'),
    stylus = require('gulp-stylus'),
    //concat = require('gulp-concat'),
    minifycss = require('gulp-minify-css'),
    clean = require('gulp-clean'),
    uglify = require('gulp-uglify'),
    //jshint = require('gulp-jshint'),
    livescript = require('gulp-livescript'),
    //cache = require('gulp-cache'),
    rename = require('gulp-rename');

// Path stuff
function src_path(path) {
  return 'packassembler/static/src/' + path;
}

function dest_path(path) {
  return 'packassembler/static/dist/' + path;
}

function compose(func1, func2) {
  return function() {
    return func1(func2.apply(null, arguments));
  };
}

var gsrc = compose(gulp.src, src_path);
var gdest = compose(gulp.dest, dest_path);

// Styles task - Compiles styl files
gulp.task('styles', function() {
  return gsrc('styles/master.styl')
    .pipe(stylus())
    .pipe(gdest('css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gdest('css'));
});

// Scripts task - Compiles livescript
gulp.task('scripts', function() {
  return gsrc('scripts/*.ls')
    .pipe(livescript({bare: true})
    .on('error', function(it){ throw it; }))
    .pipe(gdest('js'))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gdest('js'));
});

// Images task - Copies images
gulp.task('images', function() {
    return gsrc('

// Clean task - Deletes outputs
gulp.task('clean', function() {
    return gulp.src(['packassembler/static/css', 'packassembler/static/js/*.js'], {read: false}).pipe(clean());
});

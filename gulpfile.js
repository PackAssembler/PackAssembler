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
  gsrc('styles/master.styl')
    .pipe(stylus())
    .pipe(gdest('css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(gdest('css'));
});

// Scripts task - Compiles livescript
gulp.task('scripts', function() {
  gsrc('scripts/**/*.ls')
    .pipe(livescript({bare: true})
    .on('error', function(it){ throw it; }))
    .pipe(gdest('js'))
    .pipe(rename({suffix: '.min'}))
    .pipe(uglify())
    .pipe(gdest('js'));

  gsrc('scripts/lib/*').pipe(gdest('js/lib'));
});

// Images task - Copies images
gulp.task('images', function() {
  gsrc('images/**/*').pipe(gdest('img'));
});

// Clean task - Deletes outputs
gulp.task('clean', function() {
  return gulp.src([
    'packassembler/static/dist/js',
    'packassembler/static/dist/img',
    'packassembler/static/dist/css'
  ], {read: false}).pipe(clean());
});

// Default task - Clean and build all
gulp.task('default', ['clean'], function() {
  gulp.start('styles', 'scripts', 'images');
});

// Watch
gulp.task('watch', function() {
  gulp.watch(src_path('images/**/*'), ['images']);
  gulp.watch(src_path('styles/**/*'), ['styles']);
  gulp.watch(src_path('scripts/**/*'), ['scripts']);
});

// Include Gulp
var gulp = require('gulp');

// Include Our Plugins
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var autoprefixer = require('autoprefixer');
var postcss = require('gulp-postcss');

// Compile Our Sass
gulp.task('Website SCSS', function() {
  return gulp.src('collection/static/scss/style.scss')
    .pipe(sass())
    .pipe(gulp.dest('collection/static/css'));
});

gulp.task('Digested SCSS', function() {
  return gulp.src('leaguedigested/static/leaguedigested/scss/base.scss')
    .pipe(sass())
    .pipe(rename('style.css'))
    .pipe(gulp.dest('leaguedigested/static/leaguedigested/css'));
});

// Concatenate
gulp.task('scripts', function() {
  return gulp.src('collection/static/js/custom/*.js')
    .pipe(concat('all.js'))
    .pipe(gulp.dest('collection/static/js'));
});

// PostCSS processor
gulp.task('css', function () {
  var processors = [
    autoprefixer({browsers: ['last 1 version']}),
  ];
  return gulp.src('collection/static/css/*.css')
    .pipe(postcss(processors))
    .pipe(gulp.dest('collection/static/css'))
});

// Watch Files For Changes
gulp.task('watch', function() {
  gulp.watch('collection/static/js/*.js', gulp.series('scripts'));
  gulp.watch('collection/static/scss/*.scss', gulp.series('sass'));
  // gulp.watch('collection/static/css/*.css' gulp.series('css'));
});

// Default Task
gulp.task('default', gulp.series('Website SCSS', 'Digested SCSS', 'css', 'scripts'), 'watch');

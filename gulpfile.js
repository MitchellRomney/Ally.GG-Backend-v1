// Include Gulp
var gulp = require('gulp');

// Include Our Plugins
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var autoprefixer = require('autoprefixer');
var postcss = require('gulp-postcss');

gulp.task('Dashboard SCSS', function() {
  return gulp.src('dashboard/static/dashboard/scss/base.scss')
    .pipe(sass())
    .pipe(rename('style.css'))
    .pipe(gulp.dest('dashboard/static/dashboard/css'));
});

gulp.task('Dashboard Scripts', function() {
  return gulp.src('dashboard/static/dashboard/js/custom/*.js')
    .pipe(concat('all.js'))
    .pipe(gulp.dest('dashboard/static/dashboard/js'));
});

gulp.task('Dashboard CSS', function () {
  var processors = [
    autoprefixer({browsers: ['last 1 version']}),
  ];
  return gulp.src('dashboard/static/dashboard/css/*.css')
    .pipe(postcss(processors))
    .pipe(gulp.dest('dashboard/static/dashboard/css'))
});

gulp.task('Website SCSS', function() {
  return gulp.src('website/static/website/scss/base.scss')
    .pipe(sass())
    .pipe(rename('style.css'))
    .pipe(gulp.dest('website/static/website/css'));
});

gulp.task('Website Scripts', function() {
  return gulp.src('website/static/website/js/custom/*.js')
    .pipe(concat('all.js'))
    .pipe(gulp.dest('website/static/website/js'));
});

gulp.task('Website CSS', function () {
  var processors = [
    autoprefixer({browsers: ['last 1 version']}),
  ];
  return gulp.src('website/static/website/css/*.css')
    .pipe(postcss(processors))
    .pipe(gulp.dest('website/static/website/css'))
});

// Default Task
gulp.task('default', gulp.series('Dashboard SCSS', 'Dashboard Scripts', 'Dashboard CSS', 'Website SCSS', 'Website Scripts', 'Website CSS'));

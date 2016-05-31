var gulp = require('gulp');
var concat = require('gulp-concat');                            //- 多个文件合并为一个；
var minifyCss = require('gulp-minify-css');                     //- 压缩CSS为一行；
var rev = require('gulp-rev');                                  //- 对文件名加MD5后缀
var revCollector = require('gulp-rev-collector');               //- 路径替换

gulp.task('cssRev', function() {                                //- 创建一个名为 concat 的 task
    gulp.src(['./static/css/*.css'])    //- 需要处理的css文件，放到一个字符串数组里
        .pipe(minifyCss())                                      //- 压缩处理成一行
        .pipe(rev())                                            //- 文件名加MD5后缀
        .pipe(gulp.dest('./static/dist/css'))                               //- 输出文件本地
        .pipe(rev.manifest())                                   //- 生成一个rev-manifest.json
        .pipe(gulp.dest('./static/rev/css'));                              //- 将 rev-manifest.json 保存到 rev 目录内
});

gulp.task('jsRev', function() {                                //- 创建一个名为 concat 的 task
    gulp.src(['./static/js/*.js'])    //- 需要处理的css文件，放到一个字符串数组里
        .pipe(rev())                                            //- 文件名加MD5后缀
        .pipe(gulp.dest('./static/dist/js'))                               //- 输出文件本地
        .pipe(rev.manifest())                                   //- 生成一个rev-manifest.json
        .pipe(gulp.dest('./static/rev/js'));                              //- 将 rev-manifest.json 保存到 rev 目录内
});

gulp.task('rev', function() {
    gulp.src(['./static/rev/**/*.json', './templates/*.html'])   //- 读取 rev-manifest.json 文件以及需要进行css名替换的文件
        .pipe(revCollector())                                   //- 执行文件内css名的替换
        .pipe(gulp.dest('./templates/dist/'));                     //- 替换后的文件输出的目录
});

gulp.task('default', ['cssRev', 'jsRev', 'rev']);
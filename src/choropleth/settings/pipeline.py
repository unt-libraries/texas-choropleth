PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

PIPELINE_DISABLE_WRAPPER = True

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/main.less',
        ),
        'output_filename': 'css/main.min.css',
    }
}

PIPELINE_JS = {
    'map': {
        'source_filenames': (
            'js/colorbrewer.js',
            'js/map.js',
        ),
        'output_filename': 'js/map.min.js',
    },
    'app': {
        'source_filenames': (
            'js/app.js',
        ),
        'output_filename': 'js/app.min.js',
    },
    'map-vendor': {
        'source_filenames': (
            'vendor/d3/d3.js',
            'vendor/topojson/topojson.js',
            'vendor/showdown/src/showdown.js'
        ),
        'output_filename': 'js/map-vendor.min.js',
    },
    'vendor': {
        'source_filenames': (
            'vendor/angular/angular.min.js',
            'vendor/angular-resource/angular-resource.min.js',
            'vendor/jquery/dist/jquery.min.js',
            'vendor/bootstrap/dist/js/bootstrap.min.js',
        ),
        'output_filename': 'js/vendor.min.js',
    }

}

function setup
    echo "🚀 Setting up FamilyLink App..."
    echo "📦 Running 'dart pub get'..."
    dart pub get
    if test $status -ne 0
        echo "❌ 'dart pub get' failed"
        return 1
    end
    echo "🌐 Generating localization keys..."
    dart run easy_localization:generate -O lib/config/lang -f keys -o locale_keys.g.dart --source-dir ./assets/lang
    if test $status -ne 0
        echo "❌ Localization generation failed"
        return 1
    end
    echo "🔨 Running build_runner..."
    dart run build_runner build --delete-conflicting-outputs
    if test $status -ne 0
        echo "❌ Build runner failed"
        return 1
    end
    echo "✅ Setup completed successfully!"
    echo "🎉 You can now run 'flutter run' to start the app"
end

function dev
    echo "🔨 Running build_runner..."
    dart run build_runner build --delete-conflicting-outputs
end

function localize
    echo "🌐 Generating localization keys..."
    dart run easy_localization:generate -O lib/config/lang -f keys -o locale_keys.g.dart --source-dir ./assets/lang
end

function run
    if test $status -eq 0
        echo "🏃 Running the app..."
        flutter run $argv
    end
end

function dev-run
    dev
    if test $status -eq 0
        echo "🏃 Running the app..."
        flutter run $argv
    end
end

function test-app
    dev
    if test $status -eq 0
        echo "🧪 Running tests..."
        flutter test $argv
    end
end

function clean
    echo "🧹 Cleaning build artifacts..."
    dart run build_runner clean
    flutter clean
end

function pub
    echo "📦 Running 'dart pub get'..."
    dart pub get
end

function watch
    echo "👀 Starting build_runner in watch mode..."
    dart run build_runner watch --delete-conflicting-outputs
end

function flutter-help
    echo "🐟 FamilyLink App - Fish Functions"
    echo ""
    echo "Available commands:"
    echo "  setup     - Full setup (pub get + localize + build_runner)"
    echo "  dev       - Quick build_runner only"
    echo "  localize  - Generate localization keys only"
    echo "  run   - Build and run the app (with optional flags)"
    echo "  test-app  - Build and run tests"
    echo "  clean     - Clean build artifacts"
    echo "  pub       - Just dart pub get"
    echo "  watch     - Build_runner in watch mode"
    echo "  flutter-help - Show this help"
    echo ""
    echo "Usage: Just type the command name in your terminal"
end

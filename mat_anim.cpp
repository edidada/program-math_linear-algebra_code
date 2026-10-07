// Emit gnuplot commands for the same 2D transformation animation as mat_anim.rb.
#include <array>
#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

using Point = std::array<double, 2>;
using Transform = std::array<double, 4>;
Point multiply(const Transform& a, const Point& p) { return {a[0] * p[0] + a[1] * p[1], a[2] * p[0] + a[3] * p[1]}; }
Transform interpolate(const Transform& a, double t) { return {1 + t * (a[0] - 1), t * a[1], t * a[2], 1 + t * (a[3] - 1)}; }
void line(Point p, Point q, bool arrow = false, int color = 3, int width = 2) {
  std::cout << "set arrow from " << p[0] << ", " << p[1] << " to " << q[0] << ", " << q[1]
            << (arrow ? " head" : " nohead") << " lt " << color << " lw " << width << '\n';
}
int main(int argc, char** argv) {
  int frames = 50, grid = 10;
  Transform target{1, -.3, -.7, .6};
  for (int i = 1; i < argc; ++i) {
    std::string argument = argv[i];
    if ((argument == "--frame" || argument == "-f") && i + 1 < argc) frames = std::stoi(argv[++i]);
    else if (argument == "--grid" && i + 1 < argc) grid = std::stoi(argv[++i]);
    else if ((argument == "--matrix" || argument == "-a") && i + 1 < argc) {
      argument = argv[++i];
      std::replace(argument.begin(), argument.end(), ',', ' ');
      std::istringstream values(argument);
      for (double& value : target) values >> value;
    } else throw std::invalid_argument("usage: mat_anim [--frame N] [--grid N] [--matrix a,b,c,d]");
  }
  if (frames < 1 || grid < 1) throw std::invalid_argument("frame and grid must be positive");
  std::cout << std::fixed << std::setprecision(6);
  for (int frame = 0; frame <= frames; ++frame) {
    Transform current = interpolate(target, static_cast<double>(frame) / frames);
    std::cout << "set noarrow\n";
    for (int i = 0; i <= grid; ++i) {
      double x = -1 + 2.0 * i / grid;
      line(multiply(current, {x, -1}), multiply(current, {x, 1}));
      line(multiply(current, {-1, x}), multiply(current, {1, x}));
    }
    line({0, 0}, multiply(current, {1, 0}), true, 1, 5);
    line({0, 0}, multiply(current, {0, 1}), true, 1, 5);
    std::cout << "plot [-2:2][-2:2] 1/0 title ''\n";
  }
}

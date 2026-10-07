# program-math_linear-algebra_code

《程序员的数学 3：线性代数》配套示例的多语言移植。

## C++ 分支

该分支将 Ruby 示例移植为 C++17，使用 CMake 构建和 CTest 验证：

```powershell
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build --build-config Release --output-on-failure
.\build\Release\mymatrix.exe
.\build\Release\mat_anim.exe --frame 20 | gnuplot
```

`mymatrix.cpp` 保留了教材演示用的显式循环、原地 LU/带选主元 LU 分解、行列式、线性方程组与求逆算法，并以一开始就使用一的索引对应原书。

---


#### 代码来源

> http://www.ituring.com.cn/book/1239/

---

end

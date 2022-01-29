debug:
	cargo build
	ln -sf target/debug/keybrgbctl ./keybrgbctl
release:
	cargo build --release
	ln -sf target/release/keybrgbctl ./keybrgbctl
clean:
	rm -rf target/ Cargo.lock keybrgbctl
install:
    #release
	cp keybrgbctl ~/.local/bin/
	chmod +x ~/.local/bin/keybrgbctl
	echo "keybrgbctl installed in ~/.local/bin/"
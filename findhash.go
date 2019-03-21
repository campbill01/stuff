package main

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/h2non/filetype"
)

type mediaFile struct {
	path string
	hash string
}

func getSum(filename string) string {
	file, err := os.Open(filename)
	defer file.Close()
	if err != nil {
		fmt.Printf("GetSum cannot open file %s\n", err)
	}
	h := md5.New()
	defer h.Reset()
	if _, err := io.Copy(h, file); err != nil {
		fmt.Printf("Cannot generate md5 hash of %v", err)
	}
	return hex.EncodeToString(h.Sum(nil))
}

func checkType(filename string) bool {
	buf, _ := ioutil.ReadFile(filename)
	return filetype.IsImage(buf) || filetype.IsVideo(buf)
}

func catalog(dir string, wg *sync.WaitGroup, mediaFiles *[]mediaFile) {
	defer wg.Done()
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		fmt.Printf("Catalog cannot open file: %v \n", err)
	}
	for _, f := range files {
		fullpath, _ := filepath.Abs(dir + string(filepath.Separator) + f.Name())
		if !f.IsDir() {
			if checkType(fullpath) {
				sum := getSum(fullpath)
				//fmt.Printf("filename: %v, md5sum: %v\n", fullpath, sum)
				file := mediaFile{path: fullpath, hash: sum}
				*mediaFiles = append(*mediaFiles, file)
			}

		} else {
			wg.Add(1)
			// Hacky throttle.
			rand.Seed(time.Now().UnixNano())
			if rand.Int()%2 == 1 {
				go catalog(string(fullpath), wg, mediaFiles)
			} else {
				catalog(string(fullpath), wg, mediaFiles)
			}

		}
	}
}

func main() {
	var wg sync.WaitGroup
	var mediaFiles []mediaFile
	wg.Add(1)
	catalog("./", &wg, &mediaFiles)
	wg.Wait()
	for _, line := range mediaFiles {
		fmt.Println(line)
	}
}

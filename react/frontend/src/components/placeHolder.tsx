function PlaceHolder() {
  return (
    <>
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-2">
            Welcome to Our Placeholder Site
          </h2>
          <p className="mb-6">
            This is where you can describe your amazing product or service.
          </p>
          <button className="bg-white text-blue-600 py-2 px-6 rounded-full hover:bg-gray-200 transition">
            Get Started
          </button>
        </div>
      </section>

      <section className="container mx-auto px-6 py-12">
        <h3 className="text-3xl font-bold text-center mb-8">Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Feature One</h4>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Feature Two</h4>
            <p>Proin ac ligula vitae lacus posuere malesuada.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Feature Three</h4>
            <p>Quisque euismod, nisi vitae ultrices facilisis.</p>
          </div>
        </div>
      </section>

      <section className="bg-gray-100 py-12">
        <div className="container mx-auto px-6">
          <h3 className="text-3xl font-bold text-center mb-8">
            What Our Clients Say
          </h3>
          <div className="flex flex-col space-y-6 md:space-y-0 md:flex-row md:space-x-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="mb-4">
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin
                ac ligula."
              </p>
              <p className="font-semibold">— Client Name</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="mb-4">
                "Quisque euismod, nisi vitae ultrices facilisis, nisi nisi
                aliquam felis."
              </p>
              <p className="font-semibold">— Client Name</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <p className="mb-4">
                "Ullamcorper libero arcu sit amet nulla. Vivamus interdum."
              </p>
              <p className="font-semibold">— Client Name</p>
            </div>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-6 py-12">
        <h3 className="text-3xl font-bold text-center mb-8">Pricing Plans</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Basic Plan</h4>
            <p className="text-2xl font-bold mb-4">$10/month</p>
            <ul className="mb-4">
              <li>Feature One</li>
              <li>Feature Two</li>
              <li>Basic Support</li>
            </ul>
            <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
              Choose Plan
            </button>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Pro Plan</h4>
            <p className="text-2xl font-bold mb-4">$20/month</p>
            <ul className="mb-4">
              <li>All Basic Features</li>
              <li>Advanced Support</li>
              <li>Feature Three</li>
            </ul>
            <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
              Choose Plan
            </button>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h4 className="text-xl font-semibold mb-2">Enterprise Plan</h4>
            <p className="text-2xl font-bold mb-4">Contact Us</p>
            <ul className="mb-4">
              <li>All Pro Features</li>
              <li>Priority Support</li>
              <li>Custom Solutions</li>
            </ul>
            <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
              Inquire Now
            </button>
          </div>
        </div>
      </section>

      <section className="bg-gray-200 py-12">
        <div className="container mx-auto px-6 text-center">
          <h3 className="text-3xl font-bold mb-8">Contact Us</h3>
          <p className="mb-6">Have questions? We're here to help!</p>
          <form className="max-w-md mx-auto">
            <input
              type="text"
              placeholder="Your Name"
              className="w-full p-2 mb-4 border border-gray-300 rounded"
              required
            />
            <input
              type="email"
              placeholder="Your Email"
              className="w-full p-2 mb-4 border border-gray-300 rounded"
              required
            />
            <textarea
              placeholder="Your Message"
              className="w-full p-2 mb-4 border border-gray-300 rounded"
              rows={4}
              required
            />
            <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
              Send Message
            </button>
          </form>
        </div>
      </section>

      <footer className="bg-white py-4">
        <div className="container mx-auto text-center">
          <p className="text-gray-700">
            © 2024 Placeholder Site. All rights reserved.
          </p>
        </div>
      </footer>
    </>
  );
}

export default PlaceHolder;
